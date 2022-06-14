
from ctypes import addressof
from re import U
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.db.models.query_utils import Q
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail, BadHeaderError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from app1.admin import cartadmin, myaccount
from .serializers import MyTokenObtainPairSerializer
from rest_framework import generics
from . serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, GenericAPIView)
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.shortcuts import render
from app1.forms import *
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.viewsets import ModelViewSet
import pyotp
from rest_framework_simplejwt.authentication import JWTAuthentication
import json
def get_subcategory(request):
    id = request.GET.get('id', '')
    # print(id)
    result = list(subcategory.objects.filter(category_id=int(id)).values('id','sub_category'))
    # print(result)
    return HttpResponse(json.dumps(result), content_type="application/json")

def generateOTP():
    global totp
    secret = pyotp.random_base32()
    # set interval(time of the otp expiration) according to your need in seconds.
    # global totp,one_time
    totp = pyotp.TOTP(secret, interval=3000)
    one_time = totp.now()
    return one_time
# verifying OTP 

def verifyOTP(one_time):
    try:
        answer = totp.verify(one_time)
    except NameError:
        return({'msg':"OTP already used"})
    return answer
class MyPaginator(PageNumberPagination):
    
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 1000

class productview1(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = productSerializer
    pagination_class = MyPaginator
    @property
    def paginator(self):
        """The paginator instance associated with the view, or `None`."""
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator
    @property
    def paginate_queryset(self, queryset):
        """Return a single page of results, or `None` if pagination is disabled."""
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)
    @property
    def get_paginated_response(self, data):
        """Return a paginated style `Response` object for the given output data."""
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
    @property
    def list(self, request):
        query_set = Product.objects.filter(is_active=True).order_by('id')
        return self.get_paginated_response(self.serializer_class(query_set, many=True).data)
    @property   
    def retrieve(self, request, pk=None):
        item = Product.objects.filter(Q(brand_id=pk)& Q(is_active=True))
        page = self.paginate_queryset(item)
        serializer = productSerializer(item,many=True)
        return self.get_paginated_response(serializer.data)
    
def countt(request):
    usercount = User.objects.all().count()
    productcount = Product.objects.all().count()
    ordercount = Order.objects.all().count()
    context = {'usercount': usercount,
               'productcount': productcount,
               'ordercount': ordercount}
    return render(request, "admin/index.html", context)

class productsearch(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True).order_by('id')
    serializer_class = productSerializer
    pagination_class = MyPaginator
    search_fields = ['$title','$category__category','$brand__brand_name']
    filter_backends = (filters.SearchFilter,filters.OrderingFilter)
    # def list(self, request,):
    #     # page = self.paginate_queryset(self.queryset)
    #     serializer = productSerializer(self.queryset, many=True)
    #     return Response(serializer.data)
    # def retrieve(self, request, pk=None):
    #     item = Product.objects.filter(Q(brand_id=pk)& Q(is_active=True))
    #     serializer = productSerializer(item,many=True)
    #     return Response(serializer.data)
"""Serch functionality filters"""
class searchproductHitoLo(viewsets.ModelViewSet):
       queryset = Product.objects.filter(is_active=True).order_by('-price')
       serializer_class = productSerializer
       search_fields = ['title','category__category','brand__brand_name']
       filter_backends = (filters.SearchFilter,filters.OrderingFilter) 
class searchproductLotoHi(viewsets.ModelViewSet):
       queryset = Product.objects.filter(is_active=True).order_by('price')
       serializer_class = productSerializer
       search_fields = ['title','category__category','brand__brand_name']
       filter_backends = (filters.SearchFilter,filters.OrderingFilter)  
class searchnewest(viewsets.ModelViewSet):
       queryset = Product.objects.filter(is_active=True).order_by('-created_at')
       serializer_class = productSerializer
       search_fields = ['title','category__category','brand__brand_name']
       filter_backends = (filters.SearchFilter,filters.OrderingFilter)   
class searchdiscount(viewsets.ModelViewSet):
    queryset=Product.objects.filter(Q(is_active=True)& Q(discounted_price__isnull= False)).order_by('discounted_price') 
    serializer_class = productSerializer 
    pagination_class = MyPaginator  
    search_fields = ['title','category__category','brand__brand_name']
    filter_backends = (filters.SearchFilter,filters.OrderingFilter) 
    """end"""
class productview(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True).order_by('id')
    serializer_class = productSerializer
    pagination_class = MyPaginator
    search_fields = ['title','category__category','brand__brand_name']
    filter_backends = (filters.SearchFilter,filters.OrderingFilter)
    def list(self, request,):
        # page = self.paginate_queryset(self.queryset)
        serializer = productSerializer(self.queryset, many=True)
        return Response(serializer.data)
    def retrieve(self, request, pk=None):
        item = Product.objects.filter(Q(brand_id=pk)& Q(is_active=True))
        serializer = productSerializer(item,many=True)
        return Response(serializer.data)
    
class subcategoryview(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = categorySerializer01
    def list(self, request,):
        serializer = categorySerializer01(self.queryset, many=True)
        return Response(serializer.data)
    def retrieve(self, request, pk=None):
        item = Category.objects.filter(id=pk)
        serializer = categorySerializer01(item,many=True)
        return Response(serializer.data)
      
class product_brand(viewsets.ModelViewSet):
    queryset = Product
    serializer_class = productSerializer  
    pagination_class = MyPaginator
    def get_queryset(self):
        if 'pk' in self.kwargs:
            print(self.kwargs['pk'])
            print(Product.objects.filter(Q(brand_id=self.kwargs['pk'])& Q(is_active=True)))
            queryset=Product.objects.filter(Q(brand_id=self.kwargs['pk'])& Q(is_active=True))
            serializer = productSerializer(queryset,many=True)
            print(serializer.data)
            return serializer.data
        
class productHitoLo(viewsets.ModelViewSet):
       queryset = Product.objects.filter(is_active=True).order_by('-price')
       serializer_class = productSerializer
       search_fields = ['title','category__category','brand__brand_name']
       filter_backends = (filters.SearchFilter,filters.OrderingFilter)
       def list(self, request,):
           serializer = productSerializer(self.queryset, many=True)
           return Response(serializer.data)
       def retrieve(self, request, pk=None):
           item = Product.objects.filter(Q(brand_id=pk)& Q(is_active=True)).order_by('-price')
           serializer = productSerializer(item,many=True)
           return Response(serializer.data)
         
class productLotoHi(viewsets.ModelViewSet):
       queryset = Product.objects.filter(is_active=True).order_by('price')
       serializer_class = productSerializer
       search_fields = ['title','category__category','brand__brand_name']
       filter_backends = (filters.SearchFilter,filters.OrderingFilter)
       def list(self, request,):
           serializer = productSerializer(self.queryset, many=True)
           return Response(serializer.data)
       def retrieve(self, request, pk=None):
           item = Product.objects.filter(Q(brand_id=pk)& Q(is_active=True)).order_by('price')
           serializer = productSerializer(item,many=True)
           return Response(serializer.data)
       
            
class newest(viewsets.ModelViewSet):
       queryset = Product.objects.filter(is_active=True).order_by('-created_at')
       serializer_class = productSerializer
       search_fields = ['title','category__category','brand__brand_name']
       filter_backends = (filters.SearchFilter,filters.OrderingFilter)
       def list(self, request,):
           serializer = productSerializer(self.queryset, many=True)
           return Response(serializer.data)
       def retrieve(self, request, pk=None):
           item = Product.objects.filter(Q(brand_id=pk)& Q(is_active=True)).order_by('price')
           serializer = productSerializer(item,many=True)
           return Response(serializer.data)  
             
class discount(viewsets.ModelViewSet):
    queryset=Product.objects.filter(is_active=True).order_by('discounted_price') 
    serializer_class = productSerializer 
    pagination_class = MyPaginator  
    search_fields = ['title','category__category','brand__brand_name']
    filter_backends = (filters.SearchFilter,filters.OrderingFilter)
    data=Product.objects.filter(Q(is_active=True)& Q(discounted_price__isnull= False))
    def list(self,request,):
        if self.data.exists():
            queryset=Product.objects.filter(Q(is_active=True)& Q(discounted_price__isnull= False)).order_by('discounted_price') 
            queryset1=Product.objects.filter(Q(is_active=True)).order_by('discounted_price') 
            serializer = productSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            queryset=Product.objects.filter(Q(is_active=True)& Q(discounted_price__isnull= True)).order_by('discounted_price') 
            queryset1=Product.objects.filter(Q(is_active=True)).order_by('discounted_price') 
            serializer = productSerializer(queryset, many=True)
            return Response(serializer.data)
            
    def retrieve(self, request, pk=None):
        if self.data.exists():
            item = Product.objects.filter(Q(brand_id=pk)& Q(is_active=True)& Q(discounted_price__isnull= False)).order_by('price')
            serializer = productSerializer(item,many=True)
            return Response(serializer.data)
        else:
            item = Product.objects.filter(Q(brand_id=pk)& Q(is_active=True)& Q(discounted_price__isnull= True)).order_by('price')
            serializer = productSerializer(item,many=True)
            return Response(serializer.data)

class most_categoryview(viewsets.ModelViewSet):
       queryset = Product.objects.filter(is_active=True).order_by('id')
       serializer_class = productSerializer 
       def list(self, request,):
           serializer = productSerializer(self.queryset, many=True)
           return Response(serializer.data)
       def retrieve(self, request, pk=None):
           item = Product.objects.filter(category_id=pk)[:4]
           serializer = productSerializer(item,many=True)
           return Response(serializer.data)
       
class latestview(viewsets.ModelViewSet):
       queryset1 = latest_product.objects.all().order_by('id')
       queryset=Product.objects.filter(is_active=True).order_by('-created_at')[:10]
       serializer_class = productSerializer 
       search_fields = ['title','category__category','brand__brand_name']
       filter_backends = (filters.SearchFilter,filters.OrderingFilter)
    
       def list(self, request,):
           serializer = productSerializer(self.queryset, many=True)
           return Response(serializer.data)

       def retrieve(self, request, pk=None):
           item = Product.objects.filter(id=pk)
           serializer = productSerializer(item,many=True)
           return Response(serializer.data) 
       
class sidebarfilterview(APIView):
    permission_classes = (AllowAny,)
    serializer_class = sidebarfilterserializer
    def post(self, request):
        serializer = sidebarfilterserializer(data=request.data)
        subcategory_id = request.data['subcategory_id']
        brand_id = request.data['brand_id']
        attribute_id=request.data['attribute_id']
        # if attribute_id==True or brand_id==True or subcategory_id==True:
        data=Product.objects.filter(Q(attributes_id='0' if attribute_id == '' else attribute_id)| Q(brand_id='0' if brand_id == '' else brand_id)| Q(subcategory_id='0' if subcategory_id == '' else subcategory_id))
        # data1=Product.objects.filter(Q(subcategory_id=subcategory_id))
        # data2=Product.objects.filter(Q(attributes_id=attribute_id))
        # data3=Product.objects.filter(Q(brand_id=brand_id))
        # elif subcategory_id==True and attribute_id==True:
        data4=Product.objects.filter(Q(subcategory_id='0' if subcategory_id == '' else subcategory_id)& Q(attributes_id='0' if attribute_id == '' else attribute_id))
        # elif subcategory_id==True and brand_id==True:
        data5=Product.objects.filter(Q(subcategory_id='0' if subcategory_id == '' else subcategory_id)& Q(brand_id='0' if brand_id == '' else brand_id))
        # elif attribute_id==True and brand_id==True:
        data6=Product.objects.filter(Q(attributes_id='0' if attribute_id == '' else attribute_id)& Q(brand_id='0' if brand_id == '' else brand_id))
        # elif attribute_id==True and brand_id==True and subcategory_id==True:
        data7=Product.objects.filter(Q(attributes_id='0' if attribute_id == '' else attribute_id)& Q(brand_id='0' if brand_id == '' else brand_id)& Q(subcategory_id='0' if subcategory_id == '' else subcategory_id))
        
        # if data1.exists():
        #     print("data1")
        #     product_serializer=productSerializer(data1,many=True)
        # elif data2.exists():
        #     print("data2")
        #     product_serializer=productSerializer(data2,many=True)
        # elif data3.exists():
        #     print("data3")
        #     product_serializer=productSerializer(data3,many=True)
        
        if data4.exists():
            print("data4")
            product_serializer=productSerializer(data4,many=True)
        elif data5.exists():
            print("data5")
            product_serializer=productSerializer(data5,many=True)
        elif data6.exists():
            print("data6")
            product_serializer=productSerializer(data6,many=True)
        elif data7.exists():
            print("data7")
            product_serializer=productSerializer(data7,many=True)
        product_serializer=productSerializer(data,many=True)
        return Response(product_serializer.data)
    
class orderss(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    queryset = Orders.objects.all()
    serializer_class =orderserializer   
    def list(self, request,):
        queryset = Orders.objects.filter(user=self.request.user)
        serializer = orderserializer(queryset, many=True)
        return Response(serializer.data)
    def retrieve(self, request, pk=None):
        item = Orders.objects.filter(checkout_product_id=pk)
        serializer = orderserializer(item,many=True)
        return Response(serializer.data)   
           
class Listfaq(viewsets.ModelViewSet):
    queryset = FAQ.objects.filter(status="p")
    serializer_class = ffaqSerializer    
    def list(self, request,):
        serializer = ffaqSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = FAQ.objects.filter(category_id=pk)
        serializer = ffaqSerializer(item,many=True)
        return Response(serializer.data) 
      
class blogview(ViewSet):
       queryset = Blog.objects.all().order_by('id')[0:4]
       pagination_class = PageNumberPagination
       def list(self, request,):
           serializer = blogSerializer(self.queryset, many=True)
           return Response(serializer.data)

       def retrieve(self, request, pk=None):
           print(pk)
           item = Blog.objects.filter(id=pk)
        #    print(item)
           serializer = blogSerializer(item,many=True)
        #    pagination_class = PageNumberPagination
           return Response(serializer.data) 

     
class Listblog(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = blogSerializer
    
class listmyaccount(viewsets.ModelViewSet):
    # queryset = my_account.objects.all()
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = myaccountlistserializer
    def get_queryset(self):
        user = self.request.user
        return my_account.objects.filter(user=user)
      
# class myaccountCreateView1(CreateAPIView):
#     permission_classes = (IsAuthenticated, )
#     authentication_classes = [JWTAuthentication,]                      
#     serializer_class = myaccountserializers
#     queryset = my_account.objects.all()
    
class myaccountCreateView(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    queryset = my_account.objects.all()
    serializer_class = myaccountserializers
    http_method_names = ['post', ]

    def create(self, request, *args, **kwargs):
        email = request.data['email']
        print(email)
        # user = request.user
        data = {
            "msg": "Your account created Successfully",
            }
        data=my_account.objects.filter(user=self.request.user)
        serializer = self.serializer_class(data=request.data)
        if data.exists():
            return Response({'msg':'user information already exists'},status=status.HTTP_409_CONFLICT)
        else:
            if serializer.is_valid():
                print("--------------------------------",self.request.user)
                serializer.save(user=self.request.user)
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
           
            
class userphotocreate(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    queryset = userphoto.objects.all()
    serializer_class = userphotoserializer
    http_method_names = ['post', ]

    def create(self, request, *args, **kwargs):
        # user = request.user
        data = {
            "msg": "Profile photo updated successfully",
            }
        serializer = self.serializer_class(data=request.data)
        # serializer.save(user=self.request.user)
        if serializer.is_valid():
            # photoo=request.data['photo']
            # print(photoo)
            print("--------------------------------",self.request.user)
            serializer.save(user=self.request.user)
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class cartCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = cartcreateserializer
    queryset = Cart.objects.all()  
    
class cartCreateView1(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    queryset = Cart.objects.all()
    serializer_class = cartcreateserializer
    http_method_names = ['post', ]

    def create(self, request, *args, **kwargs):
        # user = request.user
        data = {
            "msg": "Added to cart succesfully",
            }
        p_id=request.data['p_id']
        data1=Product.objects.filter(id=int(p_id))
        productt=Product.objects.get(id=int(p_id))
        if data1.exists():
            serializer = self.serializer_class(data=request.data)
            # serializer.save(user=self.request.user)
            data2=Cart.objects.filter(user=self.request.user,product=productt)
            if data2.exists():
                return Response({"msg":"Product already exists in cart"},status=status.HTTP_409_CONFLICT)
            if serializer.is_valid():
                print("--------------------------------",self.request.user)
                serializer.save(user=self.request.user,product=productt)
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class cartquantityupdateView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=[JWTAuthentication,]
    def put(self, request, pk, format=None):
        # p_id=request.data['p_id']
        # productt=Product.objects.get(id=int(p_id))
        item = get_object_or_404(Cart.objects.all(), pk=pk)
        serializer = cartquantityserializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user,id=pk)
            return Response({"msg":"updated successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ordersummaryview(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=[JWTAuthentication,]
    def get(self,request):
        data1=Cart.objects.filter(user=self.request.user)
        items=[]
        amount=[]
        for i in data1:
            items.append(int(i.quantity))
            amount.append(int(i.Total_amount))
        total_items=sum(items)
        items_amount=sum(amount)
        gst=(items_amount*0.18)
        total_amount=(items_amount+gst)
        data2= [{"total_items":total_items, "items_amount": items_amount,"gst":"{:.2f}".format(gst),"total_amount":"{:.2f}".format(total_amount)}]
        results = ordersummary(data2, many=True).data
        return Response(results)
    
class checkoutsummaryview(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=[JWTAuthentication,]
    def get(self,request):
        data1=Cart.objects.filter(user=self.request.user)  
        items=[]
        amount=[]
        for i in data1:
            items.append(int(i.quantity))
            amount.append(int(i.Total_amount))
        total_items=sum(items)
        items_amount=sum(amount)
        gst=(items_amount*0.18)
        price=(items_amount+gst)
        delivery_charges=(price*0.04)
        total_payable=(price+delivery_charges)
        data2=[{"total_items":total_items,"price":price,"delivery_charges":"{:.2f}".format(delivery_charges),"total_payable":"{:.2f}".format(total_payable)}]
        results=checkoutsummary(data2,many=True).data
        return Response(results)
    
class userphoto1(viewsets.ModelViewSet):
    # queryset = my_account.objects.all()
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = userphotoserializer

    def get_queryset(self):
        user = self.request.user
        return userphoto.objects.filter(user=user)
    
class userphoto11(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = userphotoserializer
    queryset = userphoto.objects.all()  
         
# class myaccountupdateview1(UpdateAPIView):
#     permission_classes = (IsAuthenticated, )
#     authentication_classes = [JWTAuthentication,]
#     serializer_class = myaccountserializers
#     queryset = my_account.objects.all() 
    
class myaccountupdateview(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=[JWTAuthentication,]
    def put(self, request, pk, format=None):
        email=request.data['email']
        data=my_account.objects.filter(Q(user=self.request.user)& Q(email=email)& Q(is_confirmed=True))
        # data=my_account.objects.filter(email=email)
        print(data)  
        if data.exists():
            item = get_object_or_404(my_account.objects.all(), pk=pk)
            serializer = myaccountserializers(item, data=request.data)
            if serializer.is_valid():
                serializer.save(user=self.request.user)
                # my_account.objects.filter(email=email).update(
                # is_confirmed=True)
                return Response({"msg":"updated successfully"},status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        else:
            item = get_object_or_404(my_account.objects.all(), pk=pk)
            serializer = myaccountserializers(item, data=request.data)
            if serializer.is_valid():
                # if data.exists():
                #     return Response({"msg":"Entered Email id already in use"},status=status.HTTP_409_CONFLICT)
                serializer.save(user=self.request.user)
                my_account.objects.filter(user=self.request.user).update(is_confirmed=False)
                return Response({"msg":"updated successfully verify your email"},status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class myaccountemail(APIView):
    serializer_class = myaccountemailserializer
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        # password2 = handler.hash()
        if serializer.is_valid():
            email = request.data['email']
            data= my_account.objects.filter(email=email)
            if data.exists():
                subject = 'Verification OTP'
                message = 'Your Email verification OTP ' + generateOTP()
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]

                send_mail(
                    subject,
                    message,
                    email_from,
                    recipient_list,
                    fail_silently=False,
                    )
                # serializer.save(user=self.request.user)
                return Response({'msg': 'sent'}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Email not registered'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'msg': 'Not a valid request'}, status=status.HTTP_400_BAD_REQUEST)
        
class myaccountemailverify(APIView):
    permission_classes = (AllowAny,)
    serializer_class = myaccountotpsesrializer
    def post(self, request):
        # serializer = VerifyOTPSerializer(data=request.data)
        email = request.data['email']
        one_time = request.data['otp'] 
        print('one_time_password', one_time)
        one = verifyOTP(one_time)
        print('one', one)
        if one:
            my_account.objects.filter(email=email).update(
                is_confirmed=True, otp=one_time)
            return Response({'msg': 'Email verified'}, status=status.HTTP_200_OK)
        else: 
            return Response({'msg': 'OTP verfication Failed'}, status=status.HTTP_400_BAD_REQUEST)
        
class notificationlist(viewsets.ModelViewSet):
    # queryset = my_account.objects.all()
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = notificationserializer
    def get_queryset(self):
        user = self.request.user
        # return notification.objects.all()
        return notification.objects.filter(user=user)
    
class deletenotification(DestroyAPIView): 
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    def get_queryset(self):
        user = self.request.user
        # return notification.objects.all()
        return notification.objects.filter(user=user)
    
class universalnotificationlist(viewsets.ModelViewSet):
    # queryset = my_account.objects.all()
    # permission_classes = (IsAuthenticated, )
    # authentication_classes = [JWTAuthentication,]
    serializer_class = unotificationserializer
    queryset = notification.objects.all().order_by("-id")
    
class listcategory(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = categorySerializer
    
class detailcategory(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Category.objects.all()
    serializer_class=categorySerializer
    def list(self, request):
        serializer = categorySerializer(self.queryset, many=True)
        return Response(serializer.data)
    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = categorySerializer(item)
        return Response(serializer.data)
    
class listbrand(viewsets.ModelViewSet):
    queryset=Brand.objects.all()
    serializer_class=brandserializer
class listattributes(viewsets.ModelViewSet):
    queryset=Attributes.objects.all()
    serializer_class=attributesSerializer
class detailbrand(RetrieveAPIView):
    queryset=Brand.objects.all()
    serializer_class=brandserializer

class Productlist(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True).order_by('id')
    serializer_class = productSerializer
    # pagination_class = PageNumberPagination
    pagination_class = MyPaginator
    filter_fields = (
        'category',
        'brand',
    )
    
class brandproductlist(viewsets.ModelViewSet):
    queryset = Product.objects.filter(brand=2)
    serializer_class = productSerializer

class brandproductlist1(ListAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = productSerializer

    def get_queryset(self):
        brand = self.request.brand
        print("----------------------------------------------",brand)
        return Address.objects.filter(brand=brand)
    
class Productdetail(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = productSerializer
    
class latestproductlist(viewsets.ModelViewSet):
    queryset = latest_product.objects.all()
    serializer_class = latestproductserializer
    pagination_class = PageNumberPagination
    
    
class latestproductdetail(generics.RetrieveAPIView):
    queryset = latest_product.objects.all()
    serializer_class = latestproductserializer

class mostselledproductlist(viewsets.ModelViewSet):
    queryset = most_selled_products.objects.all()
    serializer_class = mostselledserializer
    pagination_class = PageNumberPagination

class mostselledproductdetail(generics.RetrieveAPIView):
    queryset = most_selled_products.objects.all()
    serializer_class = mostselledserializer

class attributelist(viewsets.ModelViewSet):
    queryset = Attributes.objects.all()

    def list(self, request):
        serializer = attributesSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = attributesSerializer(item)
        return Response(serializer.data)

    
class addresslist(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    queryset = Address.objects.all()
    serializer_class=CustomerAddressSerializers
    def list(self, request):
        queryset=Address.objects.filter(user=self.request.user).order_by("-id")
        serializer = CustomerAddressSerializers(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset=Address.objects.filter(user=self.request.user,id=pk)
        print(queryset)
        serializer = CustomerAddressSerializers(queryset,many=True)
        return Response(serializer.data)
    
class defaultaddressget(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    queryset = Address.objects.all()
    serializer_class=defaultaddressserailizer
    
    def retrieve(self, request, pk=None):
        queryset=Address.objects.filter(user=self.request.user,id=pk)
        print(queryset)
        serializer = defaultaddressserailizer(queryset,many=True)
        return Response(serializer.data)
 
class AddressCreateView1(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = CustomerAddressSerializers
    queryset = Address.objects.all()
    
class AddressCreateView(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = CustomerAddressSerializers
    queryset = Address.objects.all()
    http_method_names = ['post', ]

    def create(self, request, *args, **kwargs):
        # user = request.user
        data = {
            "msg": "Your address created Successfully",
            }
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
             
class AddressUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = CustomerAddressSerializers
    queryset = Address.objects.all()
    
# class defaultaddress1(UpdateAPIView):
#     permission_classes=(IsAuthenticated,)
#     authentication_classes=[JWTAuthentication,]
#     serializer_class=defaultaddressserailizer
#     queryset=Address.objects.all()
    
class defaultaddress(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=[JWTAuthentication,]
    def put(self, request, pk, format=None):
        item = get_object_or_404(Address.objects.all(), pk=pk)
        serializer = defaultaddressserailizer(item, data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            Address.objects.filter(user=self.request.user).update(default=False)
            Address.objects.filter(user=self.request.user,id=self.kwargs['pk']).update(default=True)
            return Response({"msg":"updated successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    
class AddressDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    queryset = Address.objects.all()
      
class attributedetail(generics.RetrieveAPIView):
    queryset = Attributes.objects.all()
    serializer_class = attributesSerializer
    
class orderlist(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    # queryset= Order.objects.filter(user=2)
    
    def list(self, request):
        serializer = ordersSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = ordersSerializer(item)
        return Response(serializer.data)
    
class orderDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    queryset = Order.objects.all()

""" class OrderDetailView(RetrieveAPIView):
    serializer_class = ordersSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            order = Order.objects.all()
            return order
        except ObjectDoesNotExist:
            raise Http404("You do not have an active order") """

class orderdetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    queryset = Order.objects.all()
    serializer_class = ordersSerializer

class orderCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = ordersSerializer
    queryset = Order.objects.all()
        
class newsletterCreateView(ModelViewSet):
    serializer_class = newsletterserializer
    queryset = newsletter.objects.all()
    http_method_names = ['post', ]
    def create(self, request, *args, **kwargs):
        # user = request.user
        data = {
            "msg": "Thank you for subscribing our newsletter",
            }
        email = request.data['Email']
        print(email)
        serializer = self.serializer_class(data=request.data)
       
        data1 = newsletter.objects.filter(Q(Email=email))
        if serializer.is_valid():
            if data1.exists():
                return Response({"msg":"You have already Subscribed our newletter"},status=status.HTTP_409_CONFLICT)
            else:
                serializer.save()
                return Response(data, status=status.HTTP_201_CREATED)
            # serializer.save()
            # return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        
class Listbanner(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = bannerSerializer
    
class Listblog(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = blogSerializer
    pagination_class = MyPaginator
    
class blogdetail(generics.RetrieveAPIView):
    # permission_classes = (IsAuthenticated, )
    queryset = Blog.objects.all()
    serializer_class = blogSerializer
    
class Listfaq1(viewsets.ModelViewSet):
    queryset = FAQ.objects.filter(status="p")
    serializer_class = ffaqSerializer
    
class faqCreateView(CreateAPIView):
    # queryset=FAQ.objects.filter(Status="Approved")
    # permission_classes = (IsAuthenticated, )
    serializer_class = faqSerializer
    queryset = FAQ.objects.all()
    
class Listrating(viewsets.ModelViewSet):
    queryset = Rating.objects.filter(Status="Approved")
    serializer_class = ratingSerializer
    
class ratingCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ratingSerializer
    queryset = Rating.objects.all()
    
class ratingupdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ratingSerializer
    queryset = Rating.objects.all()
    

class listcustomermessage(viewsets.ModelViewSet):
    queryset = customer_message.objects.all()
    serializer_class = customermessageSerializer

class customermsgCreateView(CreateAPIView):
    # permission_classes = (IsAuthenticated, )
    # authentication_classes = [JWTAuthentication,]
    serializer_class = customermessageSerializer
    queryset = customer_message.objects.all()
    
class enquiryCreateView(CreateAPIView):
    # permission_classes = (IsAuthenticated, )
    serializer_class = faq_enquirySerializer
    queryset = enquiryform.objects.all()
    
class enquirycreate(ModelViewSet):
    queryset = enquiryform.objects.all()
    serializer_class = faq_enquirySerializer
    # permission_classes = (IsAuthenticated,)
    http_method_names = ['post', ]

    def create(self, request, *args, **kwargs):
        # user = request.user
        data = {
            "msg": "Your Enquiry has been Submitted Successfully",
            }
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
          
class AddCouponView(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        code = request.data.get('code', None)
        if code is None:
            return Response({"message": "Invalid data received"}, status=HTTP_400_BAD_REQUEST)
        order = Order.objects.get(
            user=self.request.user, ordered=False)
        print("code=============================", code)
        coupon = get_object_or_404(Coupon, code=code)
        order.coupon = coupon
        order.save(*args, **kwargs)
        return Response(status=HTTP_200_OK)
    
class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

    @action(detail=True, methods=['get'])
    def redeem(self, request, pk=None):
        obj = self.get_object()
        # obj.coupon==queryset
        return Response()

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class cartlist(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = cartserializer
    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)
    # queryset = Cart.objects.all()
    # def list(self, request):
    #     serializer = cartserializer(self.queryset,many=True)
    #     return Response(serializer.data)
    # def retrieve(self, request, pk=None):
    #     item = get_object_or_404(self.queryset, pk=pk)
    #     serializer = cartserializer(item)
    #     return Response(serializer.data)
    
 
class cartDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    queryset = Cart.objects.all()
    
class cartdetail(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Cart.objects.all()
    serializer_class = cartserializer
    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)
    
class cartupdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication,]
    serializer_class = cartcreateserializer
    queryset = Cart.objects.all()
##

    
class checkoutlist(viewsets.ModelViewSet): 
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = checkoutserializer
    def get_queryset(self):
        user = self.request.user
        print("qeeeeeewqeeeeeee",user)
        return checkout.objects.filter(user=user)
    
class checkoutCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = checkoutcreateserializer
    queryset=checkout.objects.all()
    
class checkoutcouponcreate(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = checkoutcouponserializer
    queryset = checkout.objects.all()
     
class orderslist(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, )
    # authentication_classes = [JWTAuthentication,]
    serializer_class=orderserializer
    def get_queryset(self):
        user = self.request.user
        print("qeeeeeewqeeeeeee",user)
        return Orders.objects.filter(user=user)
class ordersDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    queryset = Orders.objects.all()

class ordersdetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, )
    # authentication_classes = [JWTAuthentication,]
    queryset = Orders.objects.all()
    serializer_class = orderserializer

class ordersCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = ordercreateserializer
    queryset = Orders.objects.all()
    
class ordercancelview(UpdateAPIView):
    permission_classes= (IsAuthenticated,)
    authentication_classes = [JWTAuthentication,]
    queryset=Orders.objects.all()
    serializer_class=orderscancelserializer
    
class couponredeemview(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = couponserializers
    queryset = redeemed_coupon.objects.all()
    
class socialmedialist(viewsets.ModelViewSet):
    queryset = socialmedialinks.objects.all()
    serializer_class = sociallinkserializer
    pagination_class = PageNumberPagination
  


# class CurrentUserViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = CurrentUserSerializer()
    
class CurrentUserViewSet(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    def get(self, request):
        serializer = CurrentUserSerializer(request.user)
        return Response(serializer.data)

def handler404(request,exception):
    return render(request, '404.html', status=404)

class cartorder(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    queryset = cart_order.objects.all()
    serializer_class = cartorderserializer
    http_method_names = ['post', ]

    def create(self, request, *args, **kwargs):
        # user = request.user
        data = {
            "msg": "Added to cart succesfully",
            }
        product=request.data['product']
        data1=Product.objects.filter(id=int(product))
        productt=Product.objects.get(id=int(product))
        if data1.exists():
            serializer = self.serializer_class(data=request.data)
            # serializer.save(user=self.request.user)
            data2=Cart.objects.filter(user=self.request.user,product=productt)
            if data2.exists():
                return Response({"msg":"Product already exists in cart"},status=status.HTTP_409_CONFLICT)
            if serializer.is_valid():
                print("--------------------------------",self.request.user)
                serializer.save(user=self.request.user,product=productt)
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST) 