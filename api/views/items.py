from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Item
from ..serializers import ItemSerializer
from ..filters import ItemFilter

class ItemViewSet(viewsets.ModelViewSet):
  """
  A single ViewSet for creating, listing, and managing all items,
  including Pens and PenRefills.
  """
  
  serializer_class = ItemSerializer
  queryset = Item.objects.select_related('pen', 'penrefill', 'brand', 'category').all()

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
  
