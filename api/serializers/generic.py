from rest_framework import serializers
from ..models import Memo

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

  