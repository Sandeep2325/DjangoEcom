from dataclasses import fields
from rest_framework import serializers
from . models import *
from math import ceil

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        fields="__all__"
        model=Category
class productSerializer(serializers.ModelSerializer):
    class Meta:
        fields="__all__"
        model=Product
class attributesSerializer(serializers.ModelSerializer):
    class Meta:
        fields="__all__"
        model=Attributes
class ordersSerializer(serializers.ModelSerializer):
    class Meta:
        fields="__all__"
        model=Order
