from django.contrib import admin
from .models import Record, Supplier, Product, Stock

admin.site.register(Record)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Stock)