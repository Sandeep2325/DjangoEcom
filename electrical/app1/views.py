# from urllib import response
# from rest_framework import permissions
# from rest_framework.authtoken.serializers import AuthTokenSerializer
# from django.contrib.auth import login
# from app1.models import User
# from django.shortcuts import render
# from html5lib import serialize
# from django_filters.rest_framework import DjangoFilterBackend
# from django.conf import settings
# from .filters import CouponFilter
# from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import user_passes_test
# from django.http import Http404
# from django.core.exceptions import ObjectDoesNotExist
# from rest_framework.mixins import ListModelMixin
# from re import U
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

from app1.admin import cartadmin
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
#from app1 import views

""" class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) """

def countt(request):
    usercount = User.objects.all().count()
    productcount = Product.objects.all().count()
    ordercount = Order.objects.all().count()
    context = {'usercount': usercount,
               'productcount': productcount,
               'ordercount': ordercount}
    return render(request, "admin/index.html", context)


class listmyaccount(viewsets.ModelViewSet):
    # queryset = my_account.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = myaccountlistserializer
    def get_queryset(self):
        user = self.request.user
        return my_account.objects.filter(user=user)  
class myaccountCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = myaccountserializers
    queryset = my_account.objects.all()
   
class myaccountupdateview(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = myaccountserializers
    queryset = my_account.objects.all() 
class notificationlist(viewsets.ModelViewSet):
    # queryset = my_account.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = notificationserializer
    def get_queryset(self):
        user = self.request.user
        # return notification.objects.all()
        return notification.objects.filter(user=user)

class deletenotification(DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    def get_queryset(self):
        user = self.request.user
        # return notification.objects.all()
        return notification.objects.filter(user=user)
    
class universalnotificationlist(viewsets.ModelViewSet):
    # queryset = my_account.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = unotificationserializer
    queryset = notification.objects.all()
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
class detailbrand(RetrieveAPIView):
    queryset=Brand.objects.all()
    serializer_class=brandserializer
# class Productlist(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class=productSerializer
#     pagination_class = PageNumberPagination
#     def list(self, request):
#         """ if not request.user.is_authenticated():
#             return Response({'error': 'Please Authenticate to continue'}, status=405) """
#         serializer = productSerializer(self.queryset, many=True)
#         return Response(serializer.data)
#     def retrieve(self, request, pk=None):
#         item = get_object_or_404(self.queryset, pk=pk)
#         serializer = productSerializer(item)
#         return Response(serializer.data)


class Productlist(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, )
    queryset = Product.objects.filter(is_active=True)
    # product_detail = Product.objects.get(id=id)
    # review = Rating.objects.filter(product = product_detail)
    serializer_class = productSerializer
    pagination_class = PageNumberPagination
    filter_fields = (
        'category',
        'brand',
    )

class Productdetail(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = productSerializer

class latestproductlist(viewsets.ModelViewSet):
    queryset = latest_product.objects.all()
    serializer_class = latestproductserializer
    pagination_class = PageNumberPagination
    
# class latestproductlist(viewsets.ModelViewSet):
#     # queryset=Product.objects.order_by('+id')[10]
#     queryset = latest_product.objects.all()
#     serializer_class = latestproductserializer
#     pagination_class = PageNumberPagination
    
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


class attributedetail(generics.RetrieveAPIView):
    queryset = Attributes.objects.all()
    serializer_class = attributesSerializer
      
# class orderlist(APIView):
#     permission_classes = (IsAuthenticated, )
#     def get(self, request):
#         serializer = ordersSerializer(request.user)
#         return Response(serializer.data)
    
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
    queryset = Order.objects.all()
    serializer_class = ordersSerializer


class orderCreateView(CreateAPIView):
    # permission_classes = (IsAuthenticated, )
    serializer_class = ordersSerializer
    queryset = Order.objects.all()
class AddressListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CustomerAddressSerializers

    def get_queryset(self):
        user = self.request.user

        return Address.objects.filter(user=user)

class AddressCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CustomerAddressSerializers
    queryset = Address.objects.all()

class AddressUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CustomerAddressSerializers
    queryset = Address.objects.all()

class AddressDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Address.objects.all()
class newsletterCreateView(CreateAPIView):
    # permission_classes = (IsAuthenticated, )
    serializer_class = newsletterserializer
    queryset = newsletter.objects.all()

class Listbanner(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = bannerSerializer


class Listblog(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = blogSerializer


class Listfaq(viewsets.ModelViewSet):
    queryset = FAQ.objects.filter(status="p")
    serializer_class = ffaqSerializer


class faqCreateView(CreateAPIView):
    # queryset=FAQ.objects.filter(Status="Approved")
    permission_classes = (IsAuthenticated, )
    serializer_class = faqSerializer
    queryset = FAQ.objects.all()

class Listrating(viewsets.ModelViewSet):
    queryset = Rating.objects.filter(Status="Approved")
    #queryset = Rating.objects.all()
    serializer_class = ratingSerializer
class ratingCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ratingSerializer
    queryset = Rating.objects.all()
class ratingupdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ratingSerializer
    queryset = Rating.objects.all()
    # queryset=Rating.objects.filter(Status="Approved")
    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.name = request.data.get("Rating")
    #     instance.save()
    #     serializer = self.get_serializer(instance)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)
class listcustomermessage(viewsets.ModelViewSet):
    queryset = customer_message.objects.all()
    serializer_class = customermessageSerializer

class customermsgCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = customermessageSerializer
    queryset = customer_message.objects.all()
    
class enquiryCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = faq_enquirySerializer
    queryset = enquiryform.objects.all()

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
   ######## 

class cartlist(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
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
class cartCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = cartcreateserializer
    queryset = Cart.objects.all()  
    # for i in queryset:
    #     print(i.product)     
class cartDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Cart.objects.all()
class cartdetail(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Cart.objects.all()
    serializer_class = cartserializer
    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)
class cartupdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = cartcreateserializer
    queryset = Cart.objects.all()
##
class checkoutlist(viewsets.ModelViewSet): 
    permission_classes = (IsAuthenticated, )
    serializer_class = checkoutserializer
    def get_queryset(self):
        user = self.request.user
        print("qeeeeeewqeeeeeee",user)
        return checkout.objects.filter(user=user)
class checkoutCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = checkoutcreateserializer
    queryset=checkout.objects.all()
    
class checkoutcouponcreate(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = checkoutcouponserializer
    queryset = checkout.objects.all()
     
##
class orderslist(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    # queryset = Orders.objects.all()

    # def list(self, request):
    #     serializer = orderserializer(self.queryset, many=True)
    #     return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     item = get_object_or_404(self.queryset, pk=pk)
    #     serializer = orderserializer(item)
    #     return Response(serializer.data)
    serializer_class=orderserializer
    def get_queryset(self):
        user = self.request.user
        print("qeeeeeewqeeeeeee",user)
        return Orders.objects.filter(user=user)
class ordersDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Orders.objects.all()

class ordersdetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Orders.objects.all()
    serializer_class = orderserializer

class ordersCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ordercreateserializer
    queryset = Orders.objects.all()   
class ordercancelview(UpdateAPIView):
    permission_classes= (IsAuthenticated,)
    queryset=Orders.objects.all()
    serializer_class=orderscancelserializer
    
class couponredeemview(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = couponserializers
    queryset = redeemed_coupon.objects.all()
    
class socialmedialist(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, )
    queryset = socialmedialinks.objects.all()
    # product_detail = Product.objects.get(id=id)
    # review = Rating.objects.filter(product = product_detail)
    serializer_class = sociallinkserializer
    pagination_class = PageNumberPagination
    
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "main/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com',
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/password_reset.html", context={"password_reset_form": password_reset_form})

# class CurrentUserViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = CurrentUserSerializer()
    
class CurrentUserViewSet(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        serializer = CurrentUserSerializer(request.user)
        return Response(serializer.data)

def handler404(request,exception):
    return render(request, '404.html', status=404)