from ..models import Item, Transaction, TransactionItem
from ..serializers import ItemShortSerializer
from rest_framework import serializers

# 1. This new serializer validates one line item (associative model of Transaction)
class StockUpdateLineItemSerializer(serializers.Serializer):
  item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
  quantity_change = serializers.IntegerField()
  unit_price_at_sale = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

  # check if the quantity change of an Item's transaction is zero
  def validate_quantity_change(self, value):
    if value == 0:
      raise serializers.ValidationError("Quantity change cannot be zero.")
    return value

# 2. This new serializer validates the entire batch
class BulkStockUpdateSerializer(serializers.Serializer):
  type = serializers.ChoiceField(choices=Transaction.TYPE_CHOICES)
  line_items = StockUpdateLineItemSerializer(many=True)

  # validate the line items if it is empty or there are duplicate Items
  def validate_line_items(self, value):
    if not value:
      raise serializers.ValidationError("Line items list cannot be empty.")
    
    # Check for duplicate items in the same request
    item_ids = [item_data['item'].id for item_data in value]
    if len(item_ids) != len(set(item_ids)):
      raise serializers.ValidationError("Duplicate items found in the request.")
    return value
  


class TransactionItemSerializer(serializers.ModelSerializer):
  item = ItemShortSerializer(read_only=True)
  
  class Meta:
    model = TransactionItem
    fields = ['id', 'quantity_change', 'unit_price_at_sale', 'item']

class TransactionSerializer(serializers.ModelSerializer):
  transaction_items = TransactionItemSerializer(many=True, source='line_items')

  class Meta:
    model = Transaction
    fields = ['id', 'type', 'datetime_created', 'transaction_items']