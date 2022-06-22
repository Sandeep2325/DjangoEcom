from ctypes import addressof
from multiprocessing import context
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
from .serializers import *
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
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def get_subcategory(request):
    id = request.GET.get('id', '')
    # print(id)
    result = list(subcategory.objects.filter(category_id=int(id)).values('id','sub_category'))
    print(result)
    # print(result)
    return HttpResponse(json.dumps(result), content_type="application/json")

def dashboard(request):
    products=Product.objects.all().count()
    orders=cart_order.objects.all().count()
    users=User.objects.all().count()
    
    context={
        "products":products,
        "orders":orders,
        "users":users,
    }
    print(context)
    return HttpResponse(json.dumps(context))
  
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
class userphoto1(viewsets.ModelViewSet):
    # queryset = my_account.objects.all()
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = userphotoserializer

    def get_queryset(self):
        user = self.request.user
        return userphoto.objects.filter(user=user)
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
class productsearch(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    # print(queryset)
    serializer_class = productsearchSerializer
    pagination_class = MyPaginator
    search_fields = ['$title','$category__category','$brand__brand_name',"$subcategory__sub_category"]
    filter_backends = (filters.SearchFilter,filters.OrderingFilter)         
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
class listattributes(viewsets.ModelViewSet):
    queryset=Attributes.objects.all()
    serializer_class=attributesSerializer  
class listbrand(viewsets.ModelViewSet):
    queryset=Brand.objects.all()
    serializer_class=brandserializer  

class CurrentUserViewSet(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    def get(self, request):
        serializer = CurrentUserSerializer(request.user)
        return Response(serializer.data)
class listmyaccount(viewsets.ModelViewSet):
    # queryset = my_account.objects.all()
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = myaccountlistserializer
    def get_queryset(self):
        user = self.request.user
        return my_account.objects.filter(user=user)
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
class userphoto11(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = userphotoserializer
    queryset = userphoto.objects.all()     
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
class brandproductlist1(ListAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = productSerializer

    def get_queryset(self):
        brand = self.request.brand
        print("----------------------------------------------",brand)
        return Address.objects.filter(brand=brand)
class brandproductlist(viewsets.ModelViewSet):
    queryset = Product.objects.filter(brand=2)
    serializer_class = productSerializer
class Productlist(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True).order_by('id')
    serializer_class = productSerializer
    # pagination_class = PageNumberPagination
    pagination_class = MyPaginator
    filter_fields = (
        'category',
        'brand',
    )
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
class Productdetail(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = productSerializer
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
class AddressUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = CustomerAddressSerializers
    queryset = Address.objects.all()
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
class AddCouponView(APIView):
    permission_classes = (AllowAny, )
    serializer_class=CouponSerializer
    def post(self, request, *args, **kwargs):
        serializer=CouponSerializer(data=request.data)
        coupon=request.data["coupon"]
        try:
            data=Coupon.objects.get(coupon=coupon)
            data.coupon_discount
            return Response({"data":data.coupon_discount},status=status.HTTP_202_ACCEPTED)   
        except:
            return Response({"data":"Invalid coupon"},status=status.HTTP_404_NOT_FOUND)  
class cartlist(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = cartserializer
    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)
class cartdetail(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Cart.objects.all()
    serializer_class = cartserializer
    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)
class cartDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    queryset = Cart.objects.all()  
class cartquantityupdateView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=[JWTAuthentication,]
    def put(self, request, pk, format=None):
        # p_id=request.data['p_id']
        # productt=Product.objects.get(id=int(p_id))
        item=Cart.objects.get(id=pk)
        # item = get_object_or_404(Cart.objects.all(), pk=pk)
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
        # delivery_charges=100
        total_payable=(price+delivery_charges)
        data2=[{"total_items":total_items,"price":price,"delivery_charges":"{:.2f}".format(delivery_charges),"total_payable":"{:.2f}".format(total_payable)}]
        results=checkoutsummary(data2,many=True).data
        return Response(results)
class deletenotification(DestroyAPIView): 
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    def get_queryset(self):
        user = self.request.user
        # return notification.objects.all()
        return notification.objects.filter(user=user)
# class invoice(ModelViewSet):
#     # permission_classes = (IsAuthenticated, )
#     # authentication_classes = [JWTAuthentication,]
#     queryset = cart_order.objects.all()
#     serializer_class = invoiceserializer
#     http_method_names = ['post', ]

#     def create(self, request, *args, **kwargs):
#         # user = request.user
#         data = {
#             "msg": "Added to cart succesfully",
#             }
#         buf=io.BytesIO()
#         c=canvas.Canvas(buf,pagesize=letter,bottomup=0)
#         textob=c.beginText()
#         textob.setTextOrigin(inch,inch)
#         textob.setFont("Helvetica",14)
        
#         lines=[
#             "this is line1",
#             "this is line2",
#             "this is line3",
#         ]
#         for line in lines:
#             textob.textLine(line)
#         c.drawText(textob)
#         c.showPage()
#         c.save()
#         buf.seek(0)
#         return FileResponse(buf,as_attachment=True,filename="invoice.pdf",status=status.HTTP_201_CREATED)

    
def html_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
class invoice(APIView):
    # permission_classes = (IsAuthenticated, )
    # authentication_classes = [JWTAuthentication,]
    # queryset = cart_order.objects.all()
    serializer_class = invoiceserializer
    # http_method_names = ['post', ]
    def post(self, request, *args, **kwargs):
        self.serializer_class(data=request.data)
        order_id=request.data["order_id"]
        order=cart_order.objects.get(order_payment_id=order_id)
        print(order.order_payment_id)
        data=cart2.objects.filter(order_id=order_id)
        total_amount=[]
        for i in data:
            total_amount.append(float(i.price))
        amount=sum(total_amount)   
        gst= amount*0.18
        deliver_charge=(amount+gst)*0.04
        grand_total=gst+amount+deliver_charge
        print(data)
        context_dict={
            "order_id":order.order_payment_id,
            "date":order.date,
            "total_price":amount,
            "data":data,
            "gst":gst,
            "grand_total":grand_total,
            "deliver_charge":deliver_charge
        }
    
        template_name='app1/invoice.html'
        pdf = html_to_pdf(template_name,context_dict)
        return FileResponse(pdf,as_attachment=True,filename="invoice.pdf",content_type='application/pdf',status=status.HTTP_201_CREATED)   
class filters(APIView):
    permission_classes = (AllowAny,)
    serializer_class = productfilterserializers
    def post(self, request):
        print(request.data)
        filter_by=request.data["filter_by"]
        product_id=request.data["product_id"]
        print(product_id)
        print(bool(product_id))
        attribute_id=request.data["attribute_id"]
        print(attribute_id)
        print(bool(attribute_id))
        brand_id=request.data["brand_id"]
        print(brand_id)
        print(bool(brand_id))
        subcategory_id=request.data["subcategory_id"]
        print(subcategory_id)
        print(bool(subcategory_id))
        
        if filter_by=="high_to_low":
            if bool(product_id)==True and  bool(subcategory_id)==False and bool(brand_id)==False and bool(attribute_id)==False:
                data=Product.objects.filter(id__in=product_id).order_by('-price')
                product_serializer=productSerializer(data,many=True)
                return Response(product_serializer.data)
        
            elif bool(product_id)==True and bool(attribute_id)==True and bool(subcategory_id)==False and bool(brand_id)==False:
                data1=Product.objects.filter(id__in=product_id,attributes_id__in=attribute_id).order_by('-price')
                product_serializer=productSerializer(data1,many=True)
                return Response(product_serializer.data)
            
            elif bool(product_id)==True and bool(brand_id)==True and bool(subcategory_id)==False and bool(attribute_id)==False:
                data2=Product.objects.filter(id__in=product_id,brand_id__in=brand_id).order_by('-price')
                product_serializer=productSerializer(data2,many=True)
                return Response(product_serializer.data)
            
            elif bool(product_id)==True and bool(subcategory_id)==True and bool(brand_id)==False and bool(attribute_id)==False:
                data3=Product.objects.filter(id__in=product_id,subcategory_id__in=subcategory_id).order_by('-price')
                product_serializer=productSerializer(data3,many=True)
                return Response(product_serializer.data)
            
            elif bool(product_id)==True and bool(subcategory_id)==True and bool(attribute_id)==True and bool(brand_id)==False:
                data4=Product.objects.filter(id__in=product_id,attributes_id__in=attribute_id,subcategory_id__in=subcategory_id).order_by('-price')
                product_serializer=productSerializer(data4,many=True)
                return Response(product_serializer.data)
            
            elif bool(product_id)==True and bool(attribute_id)==True and bool(brand_id)==True and bool(subcategory_id)==False:
                data5=Product.objects.filter(id__in=product_id,attributes_id__in=attribute_id,brand_id__in=brand_id).order_by('-price')
                product_serializer=productSerializer(data5,many=True)
                return Response(product_serializer.data)
            
            elif bool(product_id)==True and bool(subcategory_id)==True and bool(brand_id)==True and bool(attribute_id)==False:
                data6=Product.objects.filter(id__in=product_id,brand_id__in=brand_id,subcategory_id__in=subcategory_id).order_by('-price')
                product_serializer=productSerializer(data6,many=True)
                return Response(product_serializer.data)
            
            elif bool(product_id)==True and bool(subcategory_id)==True and bool(brand_id)==True and bool(attribute_id)==True:
                data7=Product.objects.filter(Q(id__in=product_id)& Q(attributes_id__in= attribute_id)& Q(brand_id__in=brand_id)& Q(subcategory_id__in=subcategory_id)).order_by('-price')
                product_serializer=productSerializer(data7,many=True)
                return Response(product_serializer.data)
        
        elif filter_by=="low_to_high":
            if bool(product_id)==True and  bool(subcategory_id)==False and bool(brand_id)==False and bool(attribute_id)==False:
                data=Product.objects.filter(id__in=product_id).order_by('price')
                product_serializer=productSerializer(data,many=True)
                return Response(product_serializer.data)
        
            elif bool(product_id)==True and bool(attribute_id)==True and bool(subcategory_id)==False and bool(brand_id)==False:
                data1=Product.objects.filter(id__in=product_id,attributes_id__in=attribute_id).order_by('price')
                product_serializer=productSerializer(data1,many=True)
                return Response(product_serializer.data)
            
            elif bool(product_id)==True and bool(brand_id)==True and bool(subcategory_id)==False and bool(attribute_id)==False:
                data2=Product.objects.filter(id__in=product_id,brand_id__in=brand_id).order_by('price')
                product_serializer=productSerializer(data2,many=True)
                return Response(product_serializer.data)
            
            elif bool(product_id)==True and bool(subcategory_id)==True and bool(brand_id)==False and bool(attribute_id)==False:
                data3=Product.objects.filter(id__in=product_id,subcategory_id__in=subcategory_id).order_by('price')
                product_serializer=productSerializer(data3,many=True)
                return Response(product_serializer.data)
            
            elif bool(product_id)==True and bool(subcategory_id)==True and bool(attribute_id)==True and bool(brand_id)==False:
                data4=Product.objects.filter(id__in=product_id,attributes_id__in=attribute_id,subcategory_id__in=subcategory_id).order_by('price')
                product_serializer=productSerializer(data4,many=True)
                return Response(product_serializer.data)
            
            elif bool(product_id)==True and bool(attribute_id)==True and bool(brand_id)==True and bool(subcategory_id)==False:
                data5=Product.objects.filter(id__in=product_id,attributes_id__in=attribute_id,brand_id__in=brand_id).order_by('price')
                product_serializer=productSerializer(data5,many=True)
                return Response(product_serializer.data)
            
            elif bool(product_id)==True and bool(subcategory_id)==True and bool(brand_id)==True and bool(attribute_id)==False:
                data6=Product.objects.filter(id__in=product_id,brand_id__in=brand_id,subcategory_id__in=subcategory_id).order_by('price')
                product_serializer=productSerializer(data6,many=True)
                return Response(product_serializer.data)
            
            elif bool(product_id)==True and bool(subcategory_id)==True and bool(brand_id)==True and bool(attribute_id)==True:
                data7=Product.objects.filter(Q(id__in=product_id)& Q(attributes_id__in= attribute_id)& Q(brand_id__in=brand_id)& Q(subcategory_id__in=subcategory_id)).order_by('price')
                product_serializer=productSerializer(data7,many=True)
                return Response(product_serializer.data)  
        elif filter_by=="newest":
            if bool(product_id)==True and  bool(subcategory_id)==False and bool(brand_id)==False and bool(attribute_id)==False:
                data=Product.objects.filter(id__in=product_id).order_by('-created_at')
                product_serializer=productSerializer(data,many=True)
                return Response(product_serializer.data)
        
            elif bool(product_id)==True and bool(attribute_id)==True and bool(subcategory_id)==False and bool(brand_id)==False:
                data1=Product.objects.filter(id__in=product_id,attributes_id__in=attribute_id).order_by('-created_at')
                product_serializer=productSerializer(data1,many=True)
                return Response(product_serializer.data)
            
            elif bool(product_id)==True and bool(brand_id)==True and bool(subcategory_id)==False and bool(attribute_id)==False:
                data2=Product.objects.filter(id__in=product_id,brand_id__in=brand_id).order_by('-created_at')
                product_serializer=productSerializer(data2,many=True)
                return Response(product_serializer.data)
            
            elif bool(product_id)==True and bool(subcategory_id)==True and bool(brand_id)==False and bool(attribute_id)==False:
                data3=Product.objects.filter(id__in=product_id,subcategory_id__in=subcategory_id).order_by('-created_at')
                product_serializer=productSerializer(data3,many=True)
                return Response(product_serializer.data)
            
            elif bool(product_id)==True and bool(subcategory_id)==True and bool(attribute_id)==True and bool(brand_id)==False:
                data4=Product.objects.filter(id__in=product_id,attributes_id__in=attribute_id,subcategory_id__in=subcategory_id).order_by('-created_at')
                product_serializer=productSerializer(data4,many=True)
                return Response(product_serializer.data)
            
            elif bool(product_id)==True and bool(attribute_id)==True and bool(brand_id)==True and bool(subcategory_id)==False:
                data5=Product.objects.filter(id__in=product_id,attributes_id__in=attribute_id,brand_id__in=brand_id).order_by('-created_at')
                product_serializer=productSerializer(data5,many=True)
                return Response(product_serializer.data)
            
            elif bool(product_id)==True and bool(subcategory_id)==True and bool(brand_id)==True and bool(attribute_id)==False:
                data6=Product.objects.filter(id__in=product_id,brand_id__in=brand_id,subcategory_id__in=subcategory_id).order_by('-created_at')
                product_serializer=productSerializer(data6,many=True)
                return Response(product_serializer.data)
            
            elif bool(product_id)==True and bool(subcategory_id)==True and bool(brand_id)==True and bool(attribute_id)==True:
                data7=Product.objects.filter(Q(id__in=product_id)& Q(attributes_id__in= attribute_id)& Q(brand_id__in=brand_id)& Q(subcategory_id__in=subcategory_id)).order_by('-created_at')
                product_serializer=productSerializer(data7,many=True)
                return Response(product_serializer.data)
        elif filter_by=="discount":
            pro=Product.objects.filter(Q(is_active=True)& Q(discounted_price__isnull= False))
            if pro.exists():
                if bool(product_id)==True and  bool(subcategory_id)==False and bool(brand_id)==False and bool(attribute_id)==False:
                    data=Product.objects.filter(id__in=product_id,discounted_price__isnull= False).order_by('discounted_price')
                    product_serializer=productSerializer(data,many=True)
                    return Response(product_serializer.data)
                
                elif bool(product_id)==True and bool(attribute_id)==True and bool(subcategory_id)==False and bool(brand_id)==False:
                    data1=Product.objects.filter(id__in=product_id,attributes_id__in=attribute_id,discounted_price__isnull= False).order_by('discounted_price')
                    product_serializer=productSerializer(data1,many=True)
                    return Response(product_serializer.data)
                
                elif bool(product_id)==True and bool(brand_id)==True and bool(subcategory_id)==False and bool(attribute_id)==False:
                    data2=Product.objects.filter(id__in=product_id,brand_id__in=brand_id,discounted_price__isnull= False).order_by('discounted_price')
                    product_serializer=productSerializer(data2,many=True)
                    return Response(product_serializer.data)
                
                elif bool(product_id)==True and bool(subcategory_id)==True and bool(brand_id)==False and bool(attribute_id)==False:
                    data3=Product.objects.filter(id__in=product_id,subcategory_id__in=subcategory_id,discounted_price__isnull= False).order_by('discounted_price')
                    product_serializer=productSerializer(data3,many=True)
                    return Response(product_serializer.data)
                
                elif bool(product_id)==True and bool(subcategory_id)==True and bool(attribute_id)==True and bool(brand_id)==False:
                    data4=Product.objects.filter(id__in=product_id,attributes_id__in=attribute_id,subcategory_id__in=subcategory_id,discounted_price__isnull= False).order_by('discounted_price')
                    product_serializer=productSerializer(data4,many=True)
                    return Response(product_serializer.data)
                
                elif bool(product_id)==True and bool(attribute_id)==True and bool(brand_id)==True and bool(subcategory_id)==False:
                    data5=Product.objects.filter(id__in=product_id,attributes_id__in=attribute_id,brand_id__in=brand_id,discounted_price__isnull= False).order_by('discounted_price')
                    product_serializer=productSerializer(data5,many=True)
                    return Response(product_serializer.data)
                
                elif bool(product_id)==True and bool(subcategory_id)==True and bool(brand_id)==True and bool(attribute_id)==False:
                    data6=Product.objects.filter(id__in=product_id,brand_id__in=brand_id,subcategory_id__in=subcategory_id,discounted_price__isnull= False).order_by('discounted_price')
                    product_serializer=productSerializer(data6,many=True)
                    return Response(product_serializer.data)
                
                elif bool(product_id)==True and bool(subcategory_id)==True and bool(brand_id)==True and bool(attribute_id)==True:
                    data7=Product.objects.filter(Q(id__in=product_id)& Q(attributes_id__in= attribute_id)& Q(brand_id__in=brand_id)& Q(subcategory_id__in=subcategory_id)& Q(discounted_price__isnull= False)).order_by('discounted_price')
                    product_serializer=productSerializer(data7,many=True)
                    return Response(product_serializer.data)
            else:
                if bool(product_id)==True and  bool(subcategory_id)==False and bool(brand_id)==False and bool(attribute_id)==False:
                    data=Product.objects.filter(id__in=product_id,discounted_price__isnull= True).order_by('discounted_price')
                    product_serializer=productSerializer(data,many=True)
                    return Response(product_serializer.data)
                
                elif bool(product_id)==True and bool(attribute_id)==True and bool(subcategory_id)==False and bool(brand_id)==False:
                    data1=Product.objects.filter(id__in=product_id,attributes_id__in=attribute_id,discounted_price__isnull= True).order_by('discounted_price')
                    product_serializer=productSerializer(data1,many=True)
                    return Response(product_serializer.data)
                
                elif bool(product_id)==True and bool(brand_id)==True and bool(subcategory_id)==False and bool(attribute_id)==False:
                    data2=Product.objects.filter(id__in=product_id,brand_id__in=brand_id,discounted_price__isnull= True).order_by('discounted_price')
                    product_serializer=productSerializer(data2,many=True)
                    return Response(product_serializer.data)
                
                elif bool(product_id)==True and bool(subcategory_id)==True and bool(brand_id)==False and bool(attribute_id)==False:
                    data3=Product.objects.filter(id__in=product_id,subcategory_id__in=subcategory_id,discounted_price__isnull= True).order_by('discounted_price')
                    product_serializer=productSerializer(data3,many=True)
                    return Response(product_serializer.data)
                
                elif bool(product_id)==True and bool(subcategory_id)==True and bool(attribute_id)==True and bool(brand_id)==False:
                    data4=Product.objects.filter(id__in=product_id,attributes_id__in=attribute_id,subcategory_id__in=subcategory_id,discounted_price__isnull= True).order_by('discounted_price')
                    product_serializer=productSerializer(data4,many=True)
                    return Response(product_serializer.data)
                
                elif bool(product_id)==True and bool(attribute_id)==True and bool(brand_id)==True and bool(subcategory_id)==False:
                    data5=Product.objects.filter(id__in=product_id,attributes_id__in=attribute_id,brand_id__in=brand_id,discounted_price__isnull= True).order_by('discounted_price')
                    product_serializer=productSerializer(data5,many=True)
                    return Response(product_serializer.data)
                
                elif bool(product_id)==True and bool(subcategory_id)==True and bool(brand_id)==True and bool(attribute_id)==False:
                    data6=Product.objects.filter(id__in=product_id,brand_id__in=brand_id,subcategory_id__in=subcategory_id,discounted_price__isnull= True).order_by('discounted_price')
                    product_serializer=productSerializer(data6,many=True)
                    return Response(product_serializer.data)
                
                elif bool(product_id)==True and bool(subcategory_id)==True and bool(brand_id)==True and bool(attribute_id)==True:
                    data7=Product.objects.filter(Q(id__in=product_id)& Q(attributes_id__in= attribute_id)& Q(brand_id__in=brand_id)& Q(subcategory_id__in=subcategory_id)& Q(discounted_price__isnull= True)).order_by('discounted_price')
                    product_serializer=productSerializer(data7,many=True)
                    return Response(product_serializer.data)    
class socialmedialist(viewsets.ModelViewSet):
    queryset = socialmedialinks.objects.all()
    serializer_class = sociallinkserializer
    pagination_class = PageNumberPagination
class orderview(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=[JWTAuthentication,]
    def get(self,request):
        data1=cart_order.objects.filter(user=self.request.user).order_by("-id")
        data=[]
        for i in data1:
            print(i.status)
            product_count=i.product_count
            total_price=i.total_price
            order_no=i.order_payment_id
            date=i.date
            status=i.status
            data2={"product_count":product_count,"total_price":total_price,"order_no":order_no,"date":date,"status":status}
            data.append(data2)
        # print(data)
        results=cartorderSerializer1(data,many=True).data
        return Response(results)
class orderproduct(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=[JWTAuthentication,]
    serializer_class=orderproductSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        order_id = request.data['order_id']
        data1=cart2.objects.filter(order_id=order_id)
        product_serializer=self.serializer_class(data1,many=True)
        return Response(product_serializer.data, status=status.HTTP_200_OK)
class cancelorder(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=[JWTAuthentication,]
    serializer_class=cancelorderserializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        order_id = request.data['order_id']
        data2=cart_order.objects.filter(order_payment_id=order_id,status="Delivered")
        print(data2)
        if data2.exists():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            data1=cart_order.objects.filter(order_payment_id=order_id).update(status="Cancelled")
            return Response({"msg":"Ordered Cancelled"}, status=status.HTTP_200_OK)  
class universalnotificationlist(viewsets.ModelViewSet):
    serializer_class = unotificationserializer
    queryset = notification.objects.all().order_by("-id") 
class usernotificationview(viewsets.ModelViewSet):
    permission_classes=(IsAuthenticated,)
    authentication_classes=[JWTAuthentication,]
    serializer_class = usernotificationSerializer
    queryset = notificationn.objects.all().order_by("-id")        
def handler404(request,exception):
    return render(request, '404.html', status=404)