from django.contrib import admin

# Register your models here.
from shopmanagement.models import Item

admin.site.register([Item])