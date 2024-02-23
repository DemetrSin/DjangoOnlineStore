from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from users.models import Client, Order, Review, OrderItem

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
    order_template_name = 'products/order.html'

    def get_cart_items(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart.cartitem_set.all()

    def get_total_price(self, cart_items):
        return sum(item.component.price * item.quantity for item in cart_items)

    def get_client(self, request):
        try:
            return Client.objects.get(user=request.user)
        except Client.DoesNotExist:
            return None

    def create_order(self, client, total_price):
        return Order.objects.create(
            client=client,
            order_status='New',
            order_price=total_price
        )

    def create_order_items(self, order, cart_items):
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                component=cart_item.component,
                quantity=cart_item.quantity,
                price=cart_item.component.price
            )

    def get(self, request):
        cart_items = self.get_cart_items(request)
        total_price = self.get_total_price(cart_items)
        cart_items_serializer = CartItemSerializer(cart_items, many=True)
        client = self.get_client(request)
        return render(request, self.template_name, {
            'cart_items': cart_items_serializer.data,
            'client': client,
            'total_price': total_price
        })

    def post(self, request):
        cart_items = self.get_cart_items(request)
        total_price = self.get_total_price(cart_items)
        client = self.get_client(request)
        order = self.create_order(client, total_price)
        self.create_order_items(order=order, cart_items=cart_items)
        order_items = order.order_items.all()
        Cart.objects.filter(user=self.request.user).delete()
        return render(request, self.order_template_name, {'order': order, 'order_items': order_items})


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


class BaseOrderView(View):
    template_name = None

    def get_client(self, request):
        return get_object_or_404(Client, user=request.user)

    def get_orders(self, request):
        client = self.get_client(request)
        return Order.objects.filter(client=client).all()

    def get_order(self, request, order_id):
        client = self.get_client(request)
        return get_object_or_404(Order, client=client, id=order_id)


class OrdersDetailView(BaseOrderView):
    template_name = 'products/orders_detail.html'

    def get(self, request):
        try:
            orders = self.get_orders(request)
        except Order.DoesNotExist:
            print('something')
        return render(request, self.template_name, {'orders': orders})


class OrderDetailView(BaseOrderView):
    template_name = 'products/order_detail.html'

    def get(self, request, order_id):
        try:
            order = self.get_order(request, order_id)
        except Order.DoesNotExist:
            print('something')
        return render(request, self.template_name, {'order': order})

    def post(self, request, order_id):
        return redirect('order_detail', order_id=order_id)
