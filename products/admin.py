from django.contrib import admin

from .models import Cart, Category, Component, CartItem

admin.site.register(Category)
admin.site.register(Component)
admin.site.register(Cart)
admin.site.register(CartItem)
