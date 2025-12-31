import django_filters
from .models import Item, ItemVariant, Transaction
from .constants import CATEGORY_CHOICES, STOCK_CHOICES, TYPE_CHOICES

class ItemVariantFilter(django_filters.FilterSet):
  """
  Filters for ItemVariant (the actual stockable units).
  """
  
  # 1. Filter by Item Name (looking up the parent Item model)
  name = django_filters.CharFilter(
    field_name='item__name', 
    lookup_expr='icontains', 
    label='Product Name'
  )

  # 2. Filter by Brand Name (jumping from Variant -> Item -> Brand)
  brand_name = django_filters.CharFilter(
    field_name='item__brand__name',
    lookup_expr='icontains',
    label='Brand Name'
  )

  # 3. Filter by Category (using ChoiceFilter)
  category = django_filters.ChoiceFilter(
    choices=CATEGORY_CHOICES,
    method='filter_by_category_name',
    label='Category Name'
  )

  # 4. Filter by Stock Status
  stock_status = django_filters.ChoiceFilter(
    choices=STOCK_CHOICES,
    method='filter_by_stock_status',
    label='Stock Status'
  )

  # --- DYNAMIC ATTRIBUTE FILTERS ---
  # Since attributes are in a JSONField, we can filter them like this:
  color = django_filters.CharFilter(
    field_name='attributes__color',
    lookup_expr='icontains',
    label='Color'
  )
  
  tip_size = django_filters.CharFilter(
    field_name='attributes__tip_size',
    lookup_expr='icontains',
    label='Tip Size'
  )

  class Meta:
    model = ItemVariant
    fields = ['name', 'sku']

  def filter_by_category_name(self, queryset, name, value):
    if value:
      # Filters the parent Item's category name
      return queryset.filter(item__category__name__iexact=value)
    return queryset

  def filter_by_stock_status(self, queryset, name, value):
    if value == 'in_stock':
      return queryset.filter(quantity__gt=0)
    if value == 'out_of_stock':
      return queryset.filter(quantity=0)
    return queryset


class TransactionFilter(django_filters.FilterSet):
  """
  Simplified Transaction filter using the standard field filtering.
  """
  # Since your Transaction model 'type' uses choices, 
  # we don't actually need a custom 'method' unless logic is complex.
  type = django_filters.ChoiceFilter(choices=TYPE_CHOICES)

  class Meta:
    model = Transaction
    fields = ['type']