from urllib import response
from django.shortcuts import render
from html5lib import serialize
from rest_framework import generics
from . serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from django.shortcuts import get_object_or_404
from rest_framework import viewsets


class listcategory(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class=categorySerializer


    """ def list(self, request):
        serializer = categorySerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = categorySerializer(item)
        return Response(serializer.data)
 """
""" class listcategory(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Category.objects.all()
    serializer_class=categorySerializer """
    
class detailcategory(generics.RetrieveUpdateDestroyAPIView):
    queryset=Category.objects.all()
    #serializer_class=categorySerializer
    def list(self, request):
        serializer = categorySerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = categorySerializer(item)
        return Response(serializer.data)
    
class Productlist(ViewSet):
    queryset = Product.objects.all()
    #serializer_class=productSerializer
    def list(self, request):
        serializer = productSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = productSerializer(item)
        return Response(serializer.data)

class Productdetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=productSerializer

class attributelist(ViewSet):
    queryset = Attributes.objects.all()

    def list(self, request):
        serializer = attributesSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = attributesSerializer(item)
        return Response(serializer.data)

class attributedetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Attributes.objects.all()
    serializer_class=attributesSerializer

class orderlist(ViewSet):
    queryset = Order.objects.all()

    def list(self, request):
        serializer = ordersSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = ordersSerializer(item)
        return Response(serializer.data)

class orderdetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Order.objects.all()
    serializer_class=ordersSerializer