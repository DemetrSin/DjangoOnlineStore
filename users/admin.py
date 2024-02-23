from django.contrib import admin

from .models import Client, Order, OrderItem, Review

admin.site.register(Client)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
