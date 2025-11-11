from rest_framework import filters
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Transaction
from ..serializers import TransactionSerializer
from ..pagination import CustomPageNumberPagination
from ..filters import TransactionFilter

class TransactionListView(ListAPIView):
  queryset = Transaction.objects.all()
  serializer_class = TransactionSerializer
  pagination_class = CustomPageNumberPagination

  filter_backends = [
    filters.OrderingFilter,    # For sorting (?ordering=...)
    DjangoFilterBackend,       # For filtering (?name=..., etc.)
  ]

  filterset_class = TransactionFilter

  ordering_fields = ['datetime_created']
  ordering = ['datetime_created']