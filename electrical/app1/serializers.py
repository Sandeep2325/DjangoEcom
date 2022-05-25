from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate        
from .validators import validate_username  
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from dataclasses import field, fields
import email
from enum import unique
from genericpath import exists
#from types import NoneType
from unittest.util import _MAX_LENGTH
from django.forms import CharField
from pyparsing import And
from rest_framework import serializers
import math, random
from app1.admin import ordersadmin
#from rest_auth.registration.serializers import RegisterSerializer
from . models import *
from math import ceil
from django.utils.timezone import now
from django.db import transaction
import regex as re
from collections import OrderedDict
#from app1.models import User
#from django.contrib.auth.models import User
#from .models import User
""" class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=('username','first_name','last_name','email','password','phone_no')
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],password = validated_data['password'],email=validated_data['email'],first_name=validated_data['first_name'],last_name=validated_data['last_name'],phone_no=validated_data['phone_no'])
        user.save()
        return user """
# User serializer
""" class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__' """
##################################################################################
class userserializer(serializers.ModelSerializer):
    class Meta:
        fields="__all__"
        model=User
class myaccountlistserializer(serializers.ModelSerializer):
    user=userserializer(read_only=True)
    class Meta:
        fields="__all__"
        # fields=('id','user','photo','first_name','last_name','phone_number','email','address','city','state','postal_pin')
        model=my_account
        
class myaccountserializers(serializers.ModelSerializer):
    # user=userserializer(read_only=True)
    class Meta:
        # fields=('id','user','photo','first_name','last_name','phone_number','email','address','city','state','postal_pin')
        fields="__all__"
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
class customerlistserializer(serializers.ModelSerializer):
    
    class Meta:
        fields=("id","user","fullname","phone","locality","state","city","pincode","address","home","work")
        model=Address    
class CustomerAddressSerializers(serializers.ModelSerializer):
    class Meta:
        fields = ("id","user","fullname","phone","locality","state","city","pincode","address","home","work")
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
    # def validate_address(self,value):
    #     if value=="":
    #         raise serializers.ValidationError("Please provide address")
    #     return value
    

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Category
class brandserializer(serializers.ModelSerializer):
    class Meta:
        fields="__all__"
        model=Brand 
class imageserializer(serializers.ModelSerializer):
    class Meta:
        fields="__all__"
        model=image
class productSerializer(serializers.HyperlinkedModelSerializer):
    category=categorySerializer(read_only=True)
    brand=brandserializer(read_only=True)
    image=imageserializer(many=True,read_only=True)
    class Meta:
        fields = ("id","title", "discounted_price", "category","brand","sku", "short_description", "detail_description","specification", "image","price",
                 "is_active","available_stocks", "created_at", "updated_at")
        model = Product

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['category'] = instance.category.brands
    #     response['brand']=instance.brand.brand_name
    #     response['image']=",".join([(p.image.url) for p in instance.image.all()])
        #response['image'] = instance.image.last().image.url,instance.image.first().image.url,
        # response['price'] = instance.item.price

        # return response

    def averagee_rating(self, instance):
        if Rating.objects.filter(Q(Status="Approved") & Q(product=instance)):
            review = Rating.objects.filter(Q(Status="Approved") & Q(
                product=instance)).aggregate(average=Avg('Rating'))
            avg = 0

            if review["average"] is not None:
                avg = float(review["average"])
            # return avg
            if avg != 0:
                return "%.1f" % float(avg)
            else:
                return format_html("<p class=text-danger>No ratings yet!</p>")
        else:
            return format_html("<p class=text-danger>No ratings yet!</p>")

    def count_rating(self, instance):
        if Rating.objects.filter(Q(Status="Approved") & Q(product=instance)):
            reviews = Rating.objects.filter(Q(Status="Approved") & Q(
                product=instance)).aggregate(count=Count('id'))
            cnt = 0
            if reviews["count"] is not None:
                cnt = int(reviews["count"])
            return cnt

    def reviewss(self, instance):
        if Rating.objects.filter(Q(Status="Approved") & Q(product=instance)):
            reviews = Rating.objects.filter(Q(Status="Approved") & Q(
                product=instance)).values_list("Reviews")
            for review in reviews:
                return review
        else:
            return "no ratings yet"

        # reviews=Rating.objects.filter(product=instance).values_list("Reviews")
        # for review in reviews:
        #     return review
        # reviews
class productdetailserializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Product
class latestproductserializer(serializers.ModelSerializer):
    product=productSerializer(read_only=True)
    class Meta:
        fields=("id","product","created_date")
        model=latest_product
        
class mostselledserializer(serializers.ModelSerializer):
    product=productSerializer(read_only=True)
    class Meta:
        fields = ("id","product","created_date")
        model = most_selled_products    
class attributesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Attributes
class newsletterserializer(serializers.ModelSerializer):
    class Meta:
        fields=("Email",)
        model=newsletter       
        
    def validate_Email(self,value):
        if value == "":
            raise serializers.ValidationError("Please provide email")
        return value
    
    def create(self, validate_data):
        instance = super(newsletterserializer, self).create(validate_data)
        send_mail(
            'Prakash Electricals',
            'Thank you for subscribing our Newsletter',
            settings.EMAIL_HOST_USER,
            [instance.Email],
            fail_silently=False,
        )
        return instance    
class cartcreateserializer(serializers.ModelSerializer): 
    class Meta:
        fields=('id','user','product','attributes','price','offer_price','quantity','Total_amount','amount_saved','date','updated_at')
        model=Cart
class cartserializer(serializers.ModelSerializer):
    product=productSerializer(read_only=True)
    attributes=attributesSerializer(read_only=True)
    class Meta:
        fields=('id','user','product','attributes','price','offer_price','quantity','Total_amount','amount_saved','date','updated_at')
        model=Cart
    def validate_coupon(self,value):
        list1=[]
        for coupons in Coupon.objects.all():
            a=coupons.coupon
            list1.append(a)
            b=coupons.coupon_discount

        if value!="":
            if value not in list1:
                raise serializers.ValidationError("Invalid coupon")
        return value
class checkoutcreateserializer(serializers.ModelSerializer):
    class Meta:
        model=checkout
        fields=("user","cart","Shipping_address",'No_of_items_to_checkout','checkout_amount','Coupon')
    def validate_Coupon(self,value):
        list1=[]
        for coupons in Coupon.objects.all():
            a=coupons.coupon
            list1.append(a)
            b=coupons.coupon_discount  
        if value!="":
            if value not in list1:
                raise serializers.ValidationError("Invalid coupon")
        return value 
class checkoutserializer(serializers.ModelSerializer):
    cart=cartserializer(many=True,read_only=True)
    Shipping_address=CustomerAddressSerializers(read_only=True)
    class Meta:
        model=checkout
        fields=("user","cart","Shipping_address",'No_of_items_to_checkout','checkout_amount','Coupon')
    def validate_Coupon(self,value):
        list1=[]
        for coupons in Coupon.objects.all():
            a=coupons.coupon
            list1.append(a)
            b=coupons.coupon_discount  
        if value!="":   
            if value not in list1:
                raise serializers.ValidationError("Invalid coupon")
        return value
class couponserializers(serializers.ModelSerializer):
    class Meta:
        model=redeemed_coupon
        fields=("checkout_product","coupon","redeemed_date")
    def validate_coupon(self,value):
        list1=[]
        for coupons in Coupon.objects.all():
            a=coupons.coupon
            list1.append(a)
            b=coupons.coupon_discount  
        if value!="":   
            if value not in list1:
                raise serializers.ValidationError("Invalid coupon")
        return value
                
class checkoutcouponserializer(serializers.ModelSerializer):
    class Meta:
        model=checkout
        fields=("Coupon",)
    def validate_Coupon(self,value):
        for coupons in Coupon.objects.all():
            a=coupons.coupon
            b=coupons.coupon_discount
        if value!="":
            if str(a)!=value:  
                raise serializers.ValidationError("Invalid coupon")
        return value
class ordercreateserializer(serializers.ModelSerializer):
    # checkout_product= checkoutserializer(read_only=True)
    class Meta:
        model=Orders
        fields=('id',"user","checkout_product",)
class orderserializer(serializers.ModelSerializer):
    checkout_product= checkoutserializer(read_only=True)
    class Meta:
        model=Orders
        fields=("id","user","checkout_product",)
class orderscancelserializer(serializers.ModelSerializer):
    class Meta:
        models=Orders
        fields=("id","checkout_product","status")
    def validate_status(self,value):
        pass
class ordersSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id',"user", "address", "product", 'quantity',
                  'coupon','price', 'attributes', 'status')
        model = Order
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["user"] = instance.user.username
        response["address"] = instance.address.city
        response["product"] = instance.product.title
        return response
class notificationserializer(serializers.ModelSerializer):
    class Meta:
        fields=('user_notifications','created_date')
        model=notification
class unotificationserializer(serializers.ModelSerializer):
    class Meta:
        fields=("sales","coupons")
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
        
class faqSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("Question",)
        model = FAQ
       
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
    
    # def create(self, validate_data):
    #     instance = super(faq_enquirySerializer, self).create(validate_data)
    #     send_mail(
    #         'You have a message from {}'.format(instance.name),
    #         'Name: {}\nEmail: {}\nPhone: {}\nMessage: {}'.format(instance.name,instance.Email,instance.Phone,instance.Message),
    #         settings.EMAIL_HOST_USER,
    #         ['sandeep.nexevo@gmail.com'],
    #         fail_silently=False,
    #     )
    #     return instance
    
class sociallinkserializer(serializers.ModelSerializer):
    class Meta:
        model=socialmedialinks
        fields="__all__"  
class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['user'] = user.email
        return token

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('id','username', 'password', 'password2', 'email',
                 'phone_no')
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs
    def validate_email(self, value):
        if value == None:
            raise serializers.ValidationError("Please provide email")
        return value
    # def validate_first_name(self, value):
    #     if value == None:
    #         raise serializers.ValidationError("Please provide first name")
    #     return value
    # def validate_last_name(self, value):
    #     if value == None:
    #         raise serializers.ValidationError("Please provide last name")
    #     return value
    def validate_phone_no(self, value):
        if value == None:
            raise serializers.ValidationError("Please provide phone number")
        return value 
    
    def create(self, validated_data):
        user,k = User.objects.update_or_create(
            username=validated_data['username'],
            email=validated_data['email'],
            # first_name=validated_data['first_name'],
            # last_name=validated_data['last_name'],
            phone_no=validated_data['phone_no']
        )
        def generateOTP():
            digits = "0123456789"
            OTP = ""
            for i in range(4) :
                OTP += digits[math.floor(random.random() * 10)]
            return OTP
        name=validated_data['username']
        to_email=validated_data['email']
        otp=generateOTP()
        send_mail(
            'Hi... {}'.format(name),
            'your otp is {}'.format(otp),
            settings.EMAIL_HOST_USER,
            [to_email],
            fail_silently=False,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id','password')     
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs['email'], password=attrs['password'])

        if not user:
            raise serializers.ValidationError('Incorrect email or password.')

        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')

        return {'user': user}


