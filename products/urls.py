from django.urls import path

from .api_views import CartItemListView, CartListView, CategoryListView
from .views import (AddToCartView, CartView, CatalogView, CategoryView,
                    ComponentView, RemoveFromCartView)

urlpatterns = [
    path('api/v1/categories', CategoryListView.as_view(), name='categories'),
    path('api/v1/cart', CartListView.as_view(), name='cart'),
    path('api/v1/cart_item', CartItemListView.as_view(), name='cart_item'),
    path('catalog', CatalogView.as_view(), name='catalog'),
    path('category/<slug:slug>', CategoryView.as_view(), name='category'),
    path('component/<slug:slug>', ComponentView.as_view(), name='component'),
    path('cart', CartView.as_view(), name='cart'),
    path('add_cart_item/<slug:slug>', AddToCartView.as_view(), name='add_cart_item'),
    path('remove_cart_item/<slug:slug>', RemoveFromCartView.as_view(), name='remove_cart_item')
]
