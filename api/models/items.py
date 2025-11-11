from django.db import models
from .base import Brand, Category

class Item(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=25)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  description = models.TextField(max_length=200, blank=True, null=True)
  quantity = models.IntegerField(default=0)
  target_quantity = models.PositiveIntegerField(default=0)
  brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

  def __str__(self):
    return self.name
  
  def add_stock(self, amount):
    """
    Helper function:
    Adds stock to this item and creates an 'inbound' transaction log
    """
    self.quantity += amount
    self.save(update_fields=['quantity'])
    print(f"SUCCESS LOG: Added {amount} to {self.name}. New quantity: {self.quantity}")
  
  def remove_stock(self, amount):
    """
    Helper function:
    Removes stock to this item and creates an 'outbound' transaction log
    """
    if self.quantity < amount:
      raise ValueError(f"Not enough stock for {self.name}. Have {self.quantity}, need {amount}")
    
    self.quantity -= amount
    self.save(update_fields=['quantity'])
    print(f"SUCCESS LOG: Removed {amount} to {self.name}. New quantity: {self.quantity}")


# ADD MORE depending on new item category additions

class Pen(Item):
  color = models.CharField(max_length=10)
  tip_size = models.DecimalField(max_digits=3, decimal_places=2)

class PenRefill(Item):
  color = models.CharField(max_length=10)
  tip_size = models.DecimalField(max_digits=3, decimal_places=2)