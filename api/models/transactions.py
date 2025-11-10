from django.db import models

class Transaction(models.Model):
  id = models.AutoField(primary_key=True)
  TYPE_CHOICES = [
    ('restock', 'Restock'),
    ('sale', 'Sale'),
    ('adjustment', 'Adjustment'),
  ]
  type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='sale')
  quantity_change = models.IntegerField()
  unit_price_at_sale = models.DecimalField(max_digits=10, decimal_places=2, null=True)
  datetime_created = models.DateTimeField(auto_now_add=True)
  item = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True)
