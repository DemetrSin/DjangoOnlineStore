from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import Category, Component
from .serializers import CategorySerializer, ComponentSerializer
from rest_framework import generics


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CatalogView(View):
    template_name = 'products/catalog.html'

    def get(self, request):
        categories = Category.objects.all()
        categories_serializer = CategorySerializer(categories, many=True)
        return render(request, self.template_name, {
            'categories': categories_serializer.data,
        })


class CategoryView(View):
    template_name = 'products/category.html'

    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        components = Component.objects.filter(category=category)
        components_serializer = ComponentSerializer(components, many=True)
        return render(request, self.template_name, {
            'components': components_serializer.data
        })
