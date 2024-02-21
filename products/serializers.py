from rest_framework import serializers

from .models import Category, Component


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ComponentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Component
        fields = '__all__'
