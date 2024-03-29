from django.contrib.auth.models import User
from django.db import models

from products.models import Component

ORDER_STATUS_CHOICES = (
    ('New', 'new'),
    ('In progress', 'in_progress'),
    ('The order has been sent', 'been_sent'),
    ('Delivered', 'delivered')
)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    first_name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    delivery_address = models.CharField(max_length=128)

    def __str__(self):
        return f"Client #{self.pk} > {self.user.email}"


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=30, choices=ORDER_STATUS_CHOICES)
    order_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.pk} by {self.client.first_name} {self.client.surname}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.pk}> Order Item > {self.order} > {self.component.name}"


class Review(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    review_date = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=1, choices=[(str(i), str(i)) for i in range(1, 6)])
    review_text = models.TextField()

    def __str__(self):
        return f"Review #{self.pk} by {self.client.user.username} {self.client.surname}"
