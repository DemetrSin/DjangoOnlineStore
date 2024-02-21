from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Component(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    manufacturer = models.CharField(max_length=32)
    model = models.CharField(max_length=32)
    vendor_code = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.IntegerField()
    picture = models.ImageField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pk} > {self.name}"
