from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from users.models import Client

from .forms import SearchForm
from .models import Cart, CartItem, Category, Component
from .serializers import (CartItemSerializer, CategorySerializer,
                          ComponentSerializer)


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


class CartView(View):
    template_name = 'products/cart.html'

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.cartitem_set.all()
        total_price = sum(item.component.price * item.quantity for item in cart_items)
        cart_items_serializer = CartItemSerializer(cart_items, many=True)
        try:
            client = Client.objects.get(user=request.user)
        except Client.DoesNotExist:
            client = None
        return render(request, self.template_name, {
            'cart_items': cart_items_serializer.data,
            'client': client,
            'total_price': total_price
        }
                      )


class AddToCartView(View):
    http_method_names = ['get', 'post']

    def post(self, request, slug):
        component = get_object_or_404(Component, slug=slug)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, component=component)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        messages.success(request, 'Item added to cart successfully!')
        return redirect(request.META.get('HTTP_REFERER', '/'))


class RemoveFromCartView(View):
    def post(self, request, slug):
        component = get_object_or_404(Component, slug=slug)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, component=component)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            messages.success(request, 'Item deleted from cart successfully!')
        return redirect(reverse('cart'))
