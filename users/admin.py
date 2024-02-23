from django.contrib import admin

from .models import Client, Order, Review, OrderItem

admin.site.register(Client)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
