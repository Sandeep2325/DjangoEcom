
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
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.viewsets import ModelViewSet

from rest_framework_simplejwt.authentication import JWTAuthentication

class MyPaginator(PageNumberPagination):
    
    page_size = 4
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

    def paginate_queryset(self, queryset):
        """Return a single page of results, or `None` if pagination is disabled."""
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """Return a paginated style `Response` object for the given output data."""
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
    
    def list(self, request):
        query_set = Product.objects.filter(is_active=True).order_by('id')
        return self.get_paginated_response(self.serializer_class(query_set, many=True).data)
        
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

class productview(viewsets.ModelViewSet):
    
    queryset = Product.objects.filter(is_active=True).order_by('id')
    serializer_class = productSerializer
    pagination_class = MyPaginator
    search_fields = ['title','brand','category']
    filter_backends = (filters.SearchFilter,)
    def list(self, request,):
        # page = self.paginate_queryset(self.queryset)
        serializer = productSerializer(self.queryset, many=True)
        return Response(serializer.data)
    def retrieve(self, request, pk=None):
        item = Product.objects.filter(Q(brand_id=pk)& Q(is_active=True))
        serializer = productSerializer(item,many=True)
        return Response(serializer.data)
    
class productHitoLo(viewsets.ModelViewSet):
       queryset = Product.objects.filter(is_active=True).order_by('-price')
       serializer_class = productSerializer
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
    for i in queryset: 
        def list(self,request,):
            # try:
            if self.i.discounted_price is not None:
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
            if self.i.discounted_price is not None:
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
           item = Product.objects.filter(category_id=pk)
           serializer = productSerializer(item,many=True)
           return Response(serializer.data)
       
class latestview(viewsets.ModelViewSet):
       queryset1 = latest_product.objects.all().order_by('id')
       queryset=Product.objects.filter(is_active=True).order_by('-created_at')[:10]
       serializer_class = productSerializer 
    
       def list(self, request,):
           serializer = productSerializer(self.queryset, many=True)
           return Response(serializer.data)

       def retrieve(self, request, pk=None):
           item = Product.objects.filter(id=pk)
           serializer = productSerializer(item,many=True)
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
      
class myaccountCreateView1(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]                      
    serializer_class = myaccountserializers
    queryset = my_account.objects.all()
    
class myaccountCreateView(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    queryset = my_account.objects.all()
    serializer_class = myaccountserializers
    http_method_names = ['post', ]

    def create(self, request, *args, **kwargs):
        # user = request.user
        data = {
            "msg": "Your account created Successfully",
            }
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    
               
class myaccountupdateview(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = myaccountserializers
    queryset = my_account.objects.all() 
    
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
    
class AddressListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = CustomerAddressSerializers

    def get_queryset(self):
        user = self.request.user
        return Address.objects.filter(user=user)
    
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
            serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
             
class AddressUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class = CustomerAddressSerializers
    queryset = Address.objects.all()
    
class AddressDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
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
    authentication_classes = [JWTAuthentication,]
    serializer_class = cartcreateserializer
    queryset = Cart.objects.all()  
    
    
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
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    serializer_class=orderserializer
    def get_queryset(self):
        user = self.request.user
        print("qeeeeeewqeeeeeee",user)
        return Orders.objects.filter(user=user)
    
class ordercancel(APIView):
    pass
class ordersDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
    queryset = Orders.objects.all()

class ordersdetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication,]
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
    authentication_classes = [JWTAuthentication,]
    def get(self, request):
        serializer = CurrentUserSerializer(request.user)
        return Response(serializer.data)

def handler404(request,exception):
    return render(request, '404.html', status=404)