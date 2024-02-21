from django.urls import path
from .views import CategoryListView, CatalogView, CategoryView

urlpatterns = [
    path('api/v1/categories', CategoryListView.as_view(), name='categories'),
    path('catalog', CatalogView.as_view(), name='catalog'),
    path('category/<slug:slug>', CategoryView.as_view(), name='category')
]
