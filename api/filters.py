import django_filters
from .models import Item
from .constants import CATEGORY_CHOICES, STOCK_CHOICES, TYPE_CHOICES

class ItemFilter(django_filters.FilterSet):

  STOCK_CHOICES = STOCK_CHOICES
  CATEGORY_CHOICES = CATEGORY_CHOICES

  stock_status = django_filters.ChoiceFilter(
    choices=STOCK_CHOICES,
    method='filter_by_stock_status',
    label='Stock Status'
  )

  category = django_filters.ChoiceFilter(
    choices=CATEGORY_CHOICES,
    method='filter_by_category_name',
    label='Category Name'
  )

  brand_name = django_filters.CharFilter(
    field_name='brand__name',
    lookup_expr='icontains',
    label='Brand Name'
  )

  class Meta:
    model = Item
    fields = ['name']

  def filter_by_category_name(self, queryset, name, value):
    """
    Custom filter method for the 'category__name' filter.
    """
    if value == 'pen':
      return queryset.filter(category__name="Pen")
    
    if value == 'penrefill':
      return queryset.filter(category__name="Pen Refill")
    
    return queryset

  def filter_by_stock_status(self, queryset, name, value):
    """
    Custom filter method for the 'stock_status' filter.
    """
    if value == 'in_stock':
      # This is "show items with quantities"
      return queryset.filter(quantity__gt=0)
    
    if value == 'out_of_stock':
      # This is "show items with zero quantities"
      return queryset.filter(quantity=0)
    
    # If no choice (or an invalid one) is provided, return all items
    return queryset
  
class TransactionFilter(django_filters.FilterSet):
  TYPE_CHOICES = TYPE_CHOICES

  type = django_filters.ChoiceFilter(
    choices = TYPE_CHOICES,
    method='filter_by_type',
    label='Type'
  )

  def filter_by_type(self, queryset, name, value):
    """
    Custom filter method for the transaction 'type' filter.
    """
    if value == 'sale':
      return queryset.filter(type="sale")
    elif value == 'restock':
      return queryset.filter(type="restock")
    elif value == 'adjustment':
      return queryset.filter(type="adjustment")
    else:
      return queryset
        