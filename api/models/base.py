from django.db import models

# Create your models here.



class Brand(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=25, unique=True)
  description = models.TextField(max_length=200, blank=True, null=True)

  def __str__(self):
    return self.name


class Category(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=25, unique=True)
  description = models.TextField(max_length=200, blank=True, null=True)

  attribute_schema = models.JSONField(
    default=list,
    blank=True,
    help_text="A list of required attribute keys. e.g., ['color', 'tip_size']",
  )

  def __str__(self):
    return self.name
  

class Memo(models.Model):
  id = models.AutoField(primary_key=True)
  title = models.CharField(max_length=25, unique=True)
  text = models.TextField(max_length=1000)
  datetime_created = models.DateTimeField(auto_now_add=True)
  datetime_lastupdated = models.DateTimeField(null=True)

  def __str__(self):
    return self.title