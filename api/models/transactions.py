from django.db import models

class Transaction(models.Model):
  """
  Model representing a batch operation of sales/restocks.
  Can contain multiple Items
  """
  id = models.AutoField(primary_key=True)
  TYPE_CHOICES = [
    ('restock', 'Restock'),
    ('sale', 'Sale'),
    ('adjustment', 'Adjustment'),
  ]
  type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='sale')
  datetime_created = models.DateTimeField(auto_now_add=True)
  items = models.ManyToManyField(
    'Item', 
    through='TransactionItem', 
    related_name='transactions'
  )

  def __str__(self):
    return f"{self.get_type_display()} - {self.datetime_created.strftime('%Y-%m-%d %H:%M')}"

class TransactionItem(models.Model):
  """
  Associative model for Transaction and Item
  """
  transaction = models.ForeignKey(
    Transaction,
    on_delete = models.CASCADE,
    related_name = 'line_items'
  )
  item = models.ForeignKey(
    'Item',
    on_delete = models.SET_NULL,
    null = True,
    related_name = 'transaction_lines'
  )

  quantity_change = models.IntegerField()
  unit_price_at_sale = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)

  class Meta:
    # Ensures one item only appears once per transaction batch
    unique_together = ('transaction', 'item')