
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
import math, random
#from rest_auth.registration.serializers import RegisterSerializer
from . models import *
import regex as re
from collections import OrderedDict
class userserializer(serializers.ModelSerializer):
    class Meta:
        fields="__all__"
        model=User
class myaccountlistserializer(serializers.ModelSerializer):
    # user=userserializer(read_only=True)
    class Meta:
        # fields="__all__"
        read_only_fields = ("user",) 
        fields=('id','user','first_name','last_name','phone_number','email','address','city','state','postal_pin','is_confirmed')
        model=my_account
class myaccountemailserializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ('email',)
class myaccountotpsesrializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ('email','otp')
class userphotoserializer(serializers.ModelSerializer):
    user=userserializer(read_only=True)
    class Meta:
        fields="__all__"  
        read_only_fields = ("user",) 
        model=userphoto     
class myaccountserializers(serializers.ModelSerializer):
    class Meta:
        fields="__all__"
        read_only_fields = ("user",) 
        
        model=my_account
    
    def validate_first_name(self, value):
        # if value == None:
        if value==None:
            raise serializers.ValidationError("Please enter the first name")
        return value
    def validate_last_name(self, value):
        if value == None:
            raise serializers.ValidationError("Please enter the last name")
        return value

    def validate_phone_number(self, value):
        regex=re.compile(r"\d{9}[-\.\s]??\d{9}[-\.\s]??\d{9}|\(\d{9}\)\s*\d{9}[-\.\s]??\d{9}|\d{9}[-\.\s]??\d{2}")
        if re.match(regex, str(value)):
        # if len(str(value)) !=10 :
            raise serializers.ValidationError("invalid phone number")
        return value
    def validate_email(self, value):
        # regex = re.compile(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b')
        # if re.match(regex,value):
        if value == None:
            raise serializers.ValidationError("Please enter the email address")
        return value
    def validate_address(self, value):
        if value == None:
            raise serializers.ValidationError("Please enter the address")
        return value
    def validate_city(self, value):
        if value == None:
            raise serializers.ValidationError("Please enter the city")
        return value
    def validate_state(self, value):
        if value == None:
            raise serializers.ValidationError("Please enter the state")
        return value
    def validate_postal_address(self, value):
        if value == None:
            raise serializers.ValidationError("Please enter the postal address")
        return value
 
class CustomerAddressSerializers(serializers.ModelSerializer):
    class Meta:
        fields = ("id","fullname","phone","locality","state","city","pincode","address","home","work","default")
        read_only_fields = ("user",)
        model = Address
    def validate_fullname(self, value):
        if value == "":
            raise serializers.ValidationError("Please provide Full Name")
        return value
    def validate_phone(self,value):
        if value==None:
            raise serializers.ValidationError("Please Enter phone number")
        return value
    def validate_locality(self,value):
        if value=="":
            raise serializers.ValidationError("Please Enter locality")
        return value
    
    def validate_state(self,value):
        if value=="":
            raise serializers.ValidationError("Please provide state name")
        return value
    def validate_city(self,value):
        if value=="":
            raise serializers.ValidationError("Please provide city name")
        return value
    def validate_pincode(self,value):
        if value==None:
            raise serializers.ValidationError("Please provide pincode")
        return value
    def validate_address(self,value):
        if value=="":
            raise serializers.ValidationError("Please provide address")
        return value
class defaultaddressserailizer(serializers.ModelSerializer):
    class Meta:
        fields=("default",)   
        read_only_fields=('user',)
        model = Address 
class categorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Category
class subcategoryserializer(serializers.ModelSerializer):
    class Meta:
        model=subcategory
        fields=("id","sub_category")
        depth=1
class categorySerializer01(serializers.ModelSerializer):
    subcategory=subcategoryserializer(many=True,read_only=True)
    class Meta:
        fields = ("category","subcategory")
        model = Category       
class brandserializer(serializers.ModelSerializer):
    class Meta:
        fields="__all__"
        model=Brand 
class imageserializer(serializers.ModelSerializer):
    class Meta:
        fields="__all__"
        model=image
class productsearchSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ("id","title","category","image","price","discounted_price","subcategory","attributes","brand",)
        model = Product
        depth=1
class productSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ("id","title", "discounted_price", "category","subcategory","attributes","brand","sku", "short_description", "detail_description","specification", "image","price",
                 "is_active","available_stocks", "created_at", "updated_at")
        model = Product
        depth=1

class mostselledserializer(serializers.ModelSerializer):
    product=productSerializer(read_only=True)
    class Meta:
        fields = ("id","product","created_date")
        model = most_selled_products   
         
class attributesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Attributes
        
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives,EmailMessage

class newsletterserializer(serializers.ModelSerializer):
    class Meta:
        fields=("Email",)
        model=newsletter       
    template_name = 'app1/email.html'    
    def validate_Email(self,value):
        if value == "":
            raise serializers.ValidationError("Please provide email")
        return value
    def create(self, validate_data):
        instance = super(newsletterserializer, self).create(validate_data)
        msg=EmailMessage(
            'Prakash Electricals',
            render_to_string(self.template_name),
            settings.EMAIL_HOST_USER,
            [instance.Email],
            
        )
        msg.content_subtype ="html"
        msg.send()
        return instance  
      
class cartcreateserializer(serializers.ModelSerializer):
    p_id = serializers.IntegerField()
    class Meta:
        fields=('id','p_id')
        read_only_fields = ("user","product")
        model=Cart
class cartquantityserializer(serializers.ModelSerializer):
    class Meta:
        fields=('id','quantity')
        read_only_fields=("user",)
        model=Cart
class cartcategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("category",)
        model = Category
class cartbrandserializer(serializers.ModelSerializer):
    class Meta:
        fields=("brand_name",)
        model=Brand
class cartproductSerializer(serializers.HyperlinkedModelSerializer):
    category=cartcategorySerializer(read_only=True)
    brand=cartbrandserializer(read_only=True)
    image=imageserializer(many=True,read_only=True)
    class Meta:
        fields = ("id","title", "discounted_price", "category","brand","sku","image",)
        model = Product
         
class cartserializer(serializers.ModelSerializer):
    product=cartproductSerializer(read_only=True)
    attributes=attributesSerializer(read_only=True)
    class Meta:
        fields=('id','user','product','attributes','quantity','Total_amount','updated_at')
        model=Cart
    
class ordersummary(serializers.Serializer):
   """Your data serializer, define your fields here."""
   total_items = serializers.CharField()
   items_amount = serializers.CharField()
   gst=serializers.CharField()
   total_amount=serializers.CharField()
class checkoutsummary(serializers.Serializer):
   """Your data serializer, define your fields here."""
   total_items = serializers.CharField()
   price = serializers.CharField()
   delivery_charges=serializers.CharField()
   total_payable=serializers.CharField()
class cartorderserializer(serializers.ModelSerializer):
    # cart_id=serializers.CharField()
    # address_id=serializers.CharField()
    class Meta:
        model=cart_order
        fields=("product_count","total_price","coupon")
        read_only_fields=("user","product","shipping_address")
   
class productfilterserializers(serializers.Serializer):
    brand_id = serializers.ListField()
    attribute_id=serializers.ListField()
    subcategory_id=serializers.ListField()
    product_id=serializers.ListField()
    filter_by=serializers.CharField()
class sidebarfilterserializer(serializers.Serializer):
    brand_id = serializers.ListField()
    attribute_id=serializers.ListField()
    subcategory_id=serializers.ListField()
    product_id=serializers.ListField()
class notificationserializer(serializers.ModelSerializer):
    class Meta:
        fields=('user_notifications','created_date')
        read_only_fields = ("user",)
        model=notification
class unotificationserializer(serializers.ModelSerializer):
    class Meta:
        fields=("offers",)
        read_only_fields = ("user",)
        model=notification    
    def to_representation(self, instance):
        result = super(unotificationserializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])     
class bannerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Banner
class blogSerializer(serializers.ModelSerializer):
    image=imageserializer(many=True,read_only=True)
    class Meta:
        fields = "__all__"
        fields = ("id", 'title', 'image',"detail_description",'location',"facebook","twitter","instagram","linkdin","uploaded_date")
        model = Blog

       
class ffaqSerializer(serializers.ModelSerializer):
    category=categorySerializer(read_only=True)
    class Meta:
        fields = ("id",'category','Question', 'Answer', 'created_date', 'updated_at')
        model = FAQ
        
class ratingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("user", "product", "Reviews", "Rating")
        model = Rating

    def validate_Rating(self, value):
        if value == None:
            raise serializers.ValidationError("Please rate this product")
        return value
    def validate_product(self, value):
        if value == None:
            raise serializers.ValidationError("Please select the product")
        return value

    def validate_user(self, value):
        if value == None:
            raise serializers.ValidationError("user is required")
        return value

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = instance.user.username
        #response["product"] = "product: ", instance.product.title, "category: ", instance.product.category.brands
        return response

class customermessageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = customer_message
    def validate_first_name(self, value):
        if value == "":
            raise serializers.ValidationError("Please provide first name")
        return value

    def validate_last_name(self, value):
        if value == "":
            raise serializers.ValidationError("Please provide last name")
        return value

    def validate_Email(self, value):
        # pass
        if value == None:
            raise serializers.ValidationError("Please provide your email name")
        return value

    def validate_Phone(self, value):
        # pass
        if value == None:
            raise serializers.ValidationError(
                "Please provide your mobile number")
        return value

    def validate_Message(self, value):
        if value == None:
            raise serializers.ValidationError(
                "Please provide message/ask any questions ")
        return value
 
    def create(self, validate_data):
        instance = super(customermessageSerializer, self).create(validate_data)
        send_mail(
            'You have a message from {}'.format(instance.first_name),
            'First name: {}\nLast name: {}\nEmail: {}\nPhone: {}\nMessage: {}'.format(instance.first_name,instance.last_name,instance.Email,instance.Phone,instance.Message),
            settings.EMAIL_HOST_USER,
            ['sandeep.nexevo@gmail.com'],
            fail_silently=False,
        
        )
        return instance
class faq_enquirySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = enquiryform

    def validate_name(self, value):
        if value == "":
            raise serializers.ValidationError("Please provide full name")
        return value

    def validate_Email(self, value):
        # pass
        if value == None:
            raise serializers.ValidationError("Please provide your email name")
        return value

    def validate_Phone(self, value):
        # pass
        if value == None:
            raise serializers.ValidationError(
                "Please provide your mobile number")
        return value

    def validate_Message(self, value):
        if value == None:
            raise serializers.ValidationError(
                "Please provide message/ask any questions ")
        return value
    

    
class sociallinkserializer(serializers.ModelSerializer):
    class Meta:
        model=socialmedialinks
        fields="__all__"  
class CouponSerializer(serializers.Serializer):
    coupon=serializers.CharField()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['user'] = user.email
        return token

class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id','password')     
class cartorderSerializer1(serializers.Serializer):
    order_no=serializers.CharField()
    product_count=serializers.CharField()
    total_price=serializers.CharField()
    date=serializers.CharField()
class invoiceserializer(serializers.Serializer):
    order_id=serializers.CharField()  
class orderproductSerializer(serializers.ModelSerializer):
    class Meta:
        model=cart2
        fields=("order_id","product","quantity","price")
        ready_only_fields=("user","product","quantity","price")
        depth=2

