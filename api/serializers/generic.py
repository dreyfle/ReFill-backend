from rest_framework import serializers
from ..models import Category, Brand, Memo

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
  class Meta:
    model = Brand
    fields = '__all__'

class MemoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Memo
    fields = [
      'id', 
      'title',
      'text',
      'datetime_created',
      'datetime_lastupdated', 
    ]
    read_only_fields = ['datetime_created', 'datetime_lastupdated']

  