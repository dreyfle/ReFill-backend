from django.db import transaction
from collections import defaultdict
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Item, ItemVariant, Transaction, TransactionItem
from ..serializers import ItemSerializer, ItemVariantSerializer, BulkStockUpdateSerializer
from ..filters import ItemVariantFilter
from ..pagination import CustomPageNumberPagination

class ItemViewSet(viewsets.ModelViewSet):
  """
  A single ViewSet for creating, listing, and managing all items,
  including Pens and PenRefills.
  """

  serializer_class = ItemVariantSerializer
  queryset = ItemVariant.objects.select_related('item', 'item__brand', 'item__category').all()
  pagination_class = CustomPageNumberPagination

  http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

  filter_backends = [
    filters.OrderingFilter,    # For sorting (?ordering=...)
    DjangoFilterBackend,       # For filtering (?name=..., etc.)
  ]

  filterset_class = ItemVariantFilter

  ordering_fields = ['item__name', 'price', 'quantity', 'item__brand__name', 'item__category__name']
  ordering = ['item__name']

  def get_serializer_context(self):
    context = super().get_serializer_context()
    context['request'] = self.request
    return context
  
  @action(detail=False, methods=['get'])
  def summary(self, request):
    """
    Endpoint: GET /api/items/summary/?path=category_name,brand_name,color
    """
    # 1. Get the grouping path from the URL, default to [category, brand, color]
    path_string = request.query_params.get('path', 'category_name,brand_name,color')
    group_keys = path_string.split(',')

    # 2. Fetch and serialize data
    queryset = self.filter_queryset(self.get_queryset())
    serializer = self.get_serializer(queryset, many=True)
    flat_data = serializer.data

    # 3. Dynamic Nesting Logic
    # We use a recursive function to build the tree based on the provided keys
    result = {}

    for variant in flat_data:
      self._build_dynamic_tree(result, variant, group_keys)

    return Response(result)

  def _build_dynamic_tree(self, tree, item, keys):
    """
    Helper to recursively nest data.
    """
    current_key_name = keys[0]
    
    # Pull the value from item_details or attributes
    if current_key_name in item['item_details']:
      val = item['item_details'][current_key_name]
    else:
        # Look in the dynamic JSON attributes
      val = item['attributes'].get(current_key_name, "N/A")

    # If it's the last key in the path, append the final [id, name] list
    if len(keys) == 1:
      if val not in tree:
        tree[val] = []
      
      # Format the name based on what's left
      # (In this case, just the item name and its specific SKU details)
      display_name = f"{item['item_details']['name']} ({item['sku']})"
      tree[val].append(item)
    else:
      # Otherwise, keep nesting
      if val not in tree:
        tree[val] = {}
      self._build_dynamic_tree(tree[val], item, keys[1:])
  
class BulkStockUpdateView(APIView):
  """
  An endpoint to perform bulk stock updates (add or remove).
  This creates ONE Transaction (batch) and MANY TransactionItems (lines).
  """
  
  def post(self, request, *args, **kwargs):
    # 1. Validate the whole batch
    serializer = BulkStockUpdateSerializer(data=request.data)
    if not serializer.is_valid():
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    batch_data = serializer.validated_data
    line_items_data = batch_data.pop('line_items')
    
    try:
      # 2. Use one database transaction for the whole operation
      with transaction.atomic():
        
        # --- A. UPDATE ITEM QUANTITIES ---
        
        # Lock all items in the request to prevent race conditions
        item_ids = [line['item'].id for line in line_items_data]
        items_to_update = Item.objects.select_for_update().filter(id__in=item_ids)
        item_map = {item.id: item for item in items_to_update}

        # Update quantities in memory first
        for line_data in line_items_data:
          item = item_map.get(line_data['item'].id)
          quantity = line_data['quantity_change']

          if quantity > 0:
            item.add_stock(quantity)
          elif quantity < 0:
            item.remove_stock(abs(quantity))
        
        # Now save all changed items
        # We use bulk_update for high efficiency
        Item.objects.bulk_update(items_to_update, ['quantity'])

        # --- B. CREATE AUDIT TRAIL ---
        
        # 1. Create the parent Transaction (batch)
        new_transaction = Transaction.objects.create(**batch_data)

        # 2. Create the TransactionItem (line item) objects
        line_items_to_create = []
        for line_data in line_items_data:
          line_items_to_create.append(
            TransactionItem(
              transaction=new_transaction,
              item=line_data['item'],
              quantity_change=line_data['quantity_change'],
              unit_price_at_sale=line_data.get('unit_price_at_sale')
            )
          )
        
        # Save all line items in one efficient query
        TransactionItem.objects.bulk_create(line_items_to_create)
      
      # 3. If all goes well, return success
      return Response({
        "status": "success",
        "message": f"Transaction batch created with {len(line_items_to_create)} lines."
      }, status=status.HTTP_201_CREATED)

    except ValueError as e:
      # Catch the "Not enough stock" error
      return Response({"status": "error", "detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
      # Catch any other unexpected errors
      return Response({"status": "error", "detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
