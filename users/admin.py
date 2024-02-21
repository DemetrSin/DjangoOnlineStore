from django.contrib import admin
from .models import Client, Order, Review

admin.site.register(Client)
admin.site.register(Order)
admin.site.register(Review)
