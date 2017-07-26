from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm, Textarea

# Create your models here.
class Item(models.Model):
    product_name = models.CharField(max_length=32)
    product_type = models.CharField(max_length = 20,default='mobile')
    price_per_piece = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(default=0)
    description = models.TextField(default = 'no information available')
    rating = models.PositiveIntegerField(default=0)
    positive_comments = models.PositiveIntegerField(default=0)
    total_comments = models.PositiveIntegerField(default=0)
    owner = models.ForeignKey(User)


    def __unicode__(self):
        return self.product_name


class Comment(models.Model):
    text = models.CharField(max_length=500)
    item = models.ForeignKey(Item)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.text