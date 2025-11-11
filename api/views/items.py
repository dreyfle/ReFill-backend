from django.db import transaction
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Item, Transaction, TransactionItem
from ..serializers import ItemSerializer, BulkStockUpdateSerializer
from ..filters import ItemFilter
from ..pagination import CustomPageNumberPagination

class ItemViewSet(viewsets.ModelViewSet):
  """
  A single ViewSet for creating, listing, and managing all items,
  including Pens and PenRefills.
  """

  serializer_class = ItemSerializer
  queryset = Item.objects.select_related('pen', 'penrefill', 'brand', 'category').all()
  pagination_class = CustomPageNumberPagination

  http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

  filter_backends = [
    filters.OrderingFilter,    # For sorting (?ordering=...)
    DjangoFilterBackend,       # For filtering (?name=..., etc.)
  ]

  filterset_class = ItemFilter

  ordering_fields = ['name', 'price', 'quantity', 'brand__name', 'category__name']
  ordering = ['category__name','brand__name','name']

  def get_serializer_context(self):
    context = super().get_serializer_context()
    context['request'] = self.request
    return context
  
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
