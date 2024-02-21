from django.shortcuts import get_object_or_404, render
from django.views import View
from rest_framework import generics

from .forms import SearchForm
from .models import Category, Component
from .serializers import CategorySerializer, ComponentSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CatalogView(View):
    template_name = 'products/catalog.html'

    def get(self, request):
        form = SearchForm()
        categories = Category.objects.all()
        categories_serializer = CategorySerializer(categories, many=True)
        return render(request, self.template_name, {
            'categories': categories_serializer.data,
            'form': form,
        })

    def post(self, request):
        form = SearchForm(request.POST)

        if form.is_valid():
            query = form.cleaned_data['query']
            results = Component.objects.filter(name__icontains=query)
            return render(request, self.template_name, {'form': form, 'results': results})
        return render(request, self.template_name, {'form': form})


class CategoryView(View):
    template_name = 'products/category.html'

    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        components = Component.objects.filter(category=category)
        components_serializer = ComponentSerializer(components, many=True)
        return render(request, self.template_name, {
            'components': components_serializer.data
        })


class ComponentView(View):
    template_name = 'products/component.html'

    def get(self, request, slug):
        component = Component.objects.get(slug=slug)
        component_serializer = ComponentSerializer(component)
        return render(request, self.template_name, {'component': component_serializer.data})
