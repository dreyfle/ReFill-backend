from rest_framework import serializers
from ..models import Item, ItemVariant
from .generic import CategorySerializer, BrandSerializer

class ItemSerializer(serializers.ModelSerializer):
  brand_details = BrandSerializer(source='brand', read_only=True)
  category_details = CategorySerializer(source='category', read_only=True)

  class Meta:
    model = Item
    fields = '__all__'

class ItemVariantSerializer(serializers.ModelSerializer):
  sku = serializers.CharField(read_only=True)

  category_name = serializers.CharField(source='item.category.name', read_only=True)
  brand_name = serializers.CharField(source='item.brand.name', read_only=True)
  item_name = serializers.CharField(source='item.name', read_only=True)

  brand_details = BrandSerializer(source='item.brand', read_only=True)
  category_details = CategorySerializer(source='item.category', read_only=True)

  class Meta:
    model = ItemVariant
    fields = [
      'id', 
      'item',            # ID of the parent Item
      'sku', 
      'price', 
      'quantity', 
      'target_quantity', 
      'attributes',      # The JSONField: {'color': 'Red', etc}
      
      # Helper fields for grouping
      'item_name', 
      'brand_name', 
      'category_name',
      
      # Details for the standard GET response
      'brand_details',
      'category_details'
    ]
  
  def validate(self, data):
    """
    Custom validation to ensure the JSON attributes match the Category's schema.
    """
    # If this is a partial update (PATCH) and 'attributes' isn't provided, skip
    if self.partial and 'attributes' not in data:
      return data

    # Check the model's clean() method (where we wrote the logic earlier)
    # We simulate the instance to run the model validation logic
    instance = ItemVariant(**data)
    try:
      instance.clean()
    except serializers.ValidationError as e:
      raise serializers.ValidationError(e.message_dict)
    return data

  def update(self, instance, validated_data):
    """
    Enforce the rule: Quantity cannot be updated via PATCH.
    """
    if 'quantity' in validated_data:
      raise serializers.ValidationError({
        "quantity": "Quantity can only be updated via the /stock/update/ endpoint."
      })
    return super().update(instance, validated_data)

  def to_representation(self, instance):
    """
    This formats the output to match the "item_details" 
    structure we used in the ViewSet summary action.
    """
    data = super().to_representation(instance)
    
    # We group the names into a nested object to keep the root clean
    data['item_details'] = {
      'name': data.pop('item_name'),
      'category_name': data.pop('category_name'),
      'brand_name': data.pop('brand_name'),
    }
    return data