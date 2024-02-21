import os.path

from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Component(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    manufacturer = models.CharField(max_length=32)
    model = models.CharField(max_length=32)
    vendor_code = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.IntegerField()
    picture = models.ImageField(default=os.path.join(settings.MEDIA_ROOT, 'img.png'), blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.pk} > {self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
