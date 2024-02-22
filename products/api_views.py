from rest_framework import generics

from products.models import Cart, CartItem, Category
from products.serializers import (CartItemSerializer, CartSerializer,
                                  CategorySerializer)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CartListView(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemListView(generics.ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
