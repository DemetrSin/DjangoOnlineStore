from rest_framework import serializers

from .models import Cart, CartItem, Category, Component


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ComponentSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Component
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer()
    component = ComponentSerializer()

    class Meta:
        model = CartItem
        fields = '__all__'