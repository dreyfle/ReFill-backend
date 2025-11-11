from rest_framework import serializers
from ..models import Category, Brand, Pen, PenRefill, Item
from .generic import CategorySerializer, BrandSerializer


class PenSerializer(serializers.ModelSerializer):
  # --- For WRITE (PATCH/POST) ---
  # Accepts an ID, e.g., "brand": 1
  brand = serializers.PrimaryKeyRelatedField(
    queryset=Brand.objects.all(), 
  )
  category = serializers.PrimaryKeyRelatedField(
    queryset=Category.objects.all(), 
  )

  # -- For READ (GET) ---
  brand_details = BrandSerializer(source='brand', read_only=True)
  category_details = CategorySerializer(source='category', read_only=True)

  class Meta:
    model = Pen
    fields = "__all__"

class PenRefillSerializer(serializers.ModelSerializer):
  # --- For WRITE (PATCH/POST) ---
  # Accepts an ID, e.g., "brand": 1
  brand = serializers.PrimaryKeyRelatedField(
    queryset=Brand.objects.all(), 
  )
  category = serializers.PrimaryKeyRelatedField(
    queryset=Category.objects.all(), 
  )

  # -- For READ (GET) ---
  brand_details = BrandSerializer(source='brand', read_only=True)
  category_details = CategorySerializer(source='category', read_only=True)

  class Meta:
    model = PenRefill
    fields = "__all__"



class ItemSerializer(serializers.ModelSerializer):
  # WRITE-ONLY FIELDS (FOR INPUT)
  brand = serializers.PrimaryKeyRelatedField(
    queryset = Brand.objects.all().order_by('name'), 
    write_only = True
  )
  category = serializers.PrimaryKeyRelatedField(
    queryset = Category.objects.all().order_by('name'), 
    write_only = True
  )
  color = serializers.CharField(max_length=10, required=False, allow_null=True, write_only=True)
  tip_size = serializers.DecimalField(max_digits=3, decimal_places=2, required=False, allow_null=True, write_only=True)


  class Meta:
    model = Item
    fields = [
      'id','name','price','description','quantity','target_quantity',
      # Input (POST/PATCH) fields
      'brand','category',
      # Sub-class fields
      # for Pen and Pen Refill
      'color','tip_size'
    ]

  def create(self, validated_data):
    # FACTORY design
    category = validated_data.get('category')

    if category.name == "Pen":
      model_class = Pen
    elif category.name == "Pen Refill":
      model_class = PenRefill
    else:
      model_class = Item

    # Get all valid field names for model_class
    valid_field_names = {f.name for f in model_class._meta.get_fields()}
    
    # Filter the validated_data
    filtered_data = {
      key: value for key, value in validated_data.items()
      if key in valid_field_names
    }

    # Create the correct object
    return model_class.objects.create(**filtered_data)

  def update(self, instance, validated_data):
    if 'quantity' in validated_data:
      raise serializers.ValidationError({
        'quantity': 'Cannot update quantity directly. Please use a different endpoint to add/remove stock.'
      })

    # Get the raw request data
    request_data = self.context['request'].data
    
    # Find the correct instance and serializer
    if hasattr(instance, 'pen'):
      target_instance = instance.pen
      serializer_class = PenSerializer
    elif hasattr(instance, 'penrefill'):
      target_instance = instance.penrefill
      serializer_class = PenRefillSerializer
    else:
      target_instance = instance
      serializer_class = ItemSerializer

    # Initialize the correct serializer with the correct child instance.
    serializer = serializer_class(
      target_instance, 
      data=request_data, 
      partial=True
    )
    
    # Let the child serializer do ALL validation and saving
    if serializer.is_valid(raise_exception=True):
      return serializer.save()
        
    return instance
  
  def to_representation(self, instance):
    """
    It checks the instance type and uses the correct serializer.
    """

    if hasattr(instance, 'pen'):
      # Use PenSerializer to format the output
      return PenSerializer(instance.pen).data
    
    elif hasattr(instance, 'penrefill'):
      # Use PenRefillSerializer to format the output
      return PenRefillSerializer(instance.penrefill).data
    
    else:
      # Use the base ItemSerializer
      return ItemSerializer(instance).data

class ItemShortSerializer(serializers.ModelSerializer):
  class Meta:
    model = Item
    fields = ['id', 'name', 'description', 'brand', 'category']