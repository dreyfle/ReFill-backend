from django.db import models

# Create your models here.



class Brand(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=25, unique=True)
  description = models.TextField(max_length=200)

  def __str__(self):
    return self.name


class Category(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=25, unique=True)
  description = models.TextField(max_length=200)

  def __str__(self):
    return self.name
  

class Memo(models.Model):
  id = models.AutoField(primary_key=True)
  title = models.CharField(max_length=25, unique=True)
  text = models.TextField(max_length=1000)
  datetime_created = models.DateTimeField(auto_now_add=True)
  datetime_lastupdated = models.DateTimeField(null=True)