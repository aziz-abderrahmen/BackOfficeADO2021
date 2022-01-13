from django.db import models
import datetime

# Create your models here.
class InfoProduct(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    tig_id = models.IntegerField(default='-1')
    name = models.CharField(max_length=100, blank=True, default='')
    category = models.IntegerField(default='-1')
    price = models.FloatField(default='0')
    unit = models.CharField(max_length=20, blank=True, default='')
    availability = models.BooleanField(default=True)
    sale = models.BooleanField(default=False)
    discount = models.FloatField(default='0')
    comments = models.CharField(max_length=100, blank=True, default='')
    owner = models.CharField(max_length=20, blank=True, default='tig_orig')
    quantityInStock = models.IntegerField(default='0')
    nombre_produit_vendu = models.IntegerField(default='0')
    sell_price = models.IntegerField(default='0')
    
    class Meta:
        ordering = ('name',)


class Transaction(models.Model):
    created = models.DateTimeField(default=datetime.datetime.now())
    price = models.FloatField(default='0')
    quantity = models.IntegerField(default='0')
    tig_id = models.IntegerField(default='-1')
    type = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ('created',)


   
        