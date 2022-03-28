from django.contrib.auth.password_validation import validate_password
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

from app1.admin import ordersadmin
#from rest_auth.registration.serializers import RegisterSerializer
from . models import *
from math import ceil
from django.utils.timezone import now
from django.db import transaction
import regex as re
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
# class userserializer(serializers.ModelSerializer):
#     class Meta:
#         fields="__all__"
class myaccountserializers(serializers.ModelSerializer):
    class Meta:
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
    
class CustomerAddressSerializers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Address
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # # user=serializers.PrimaryKeyRelatedField(max_length=200)
    # door_number = serializers.IntegerField()
    # street = serializers.CharField(max_length=300)
    # city = serializers.CharField(max_length=300)
    # state = serializers.CharField(max_length=300)
    # country = serializers.CharField(max_length=300)
    # pincode = serializers.IntegerField()
    # phone_no = serializers.IntegerField()

    
    def validate_door_number(self, value):
        if value == None:
            raise serializers.ValidationError("please enter the door number")
        return value
    
    # def validate(self, attrs):
    #     if attrs['door_number'] in NULL:
    #         raise serializers.ValidationError(
    #             {"door_number": "field required."})

    #     return attrs
    
    # def to_representation(self, instance):
    #     response=super().to_representation(instance)
    #     response["user"]=instance.user.username
    #     return response


class categorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Category

    # def get_photo_url(self, Category):
    #     request = self.context.get('request')
    #     photo_url = Category.category_image.url
    #     return request.build_absolute_uri(photo_url)
class productSerializer(serializers.ModelSerializer):
    #category_name = serializers.RelatedField(source='category.name', read_only=True)
    #category = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        fields = ("id", "title", "discounted_price", "category","brand","sku", "short_description", "detail_description", "image", "product_image", "price",
                 "is_active", "created_at", "updated_at", "average_rating", "count_review", "reviews")
        model = Product

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['category'] = instance.category.brands
        response['brand']=instance.brand.brand_name
        response['image']=",".join([(p.image.url) for p in instance.image.all()])
        #response['image'] = instance.image.last().image.url,instance.image.first().image.url,
        # response['price'] = instance.item.price

        return response

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
            # return format_html("<p class=text-danger>No ratings yet!</p>")
            return "no ratings yet"

        # reviews=Rating.objects.filter(product=instance).values_list("Reviews")
        # for review in reviews:
        #     return review
        # reviews

class productdetailserializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Product

class attributesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Attributes
        
class cartserializer(serializers.ModelSerializer):
    class Meta:
        fields=('id','user','product','attributes','price','offer_price','coupon','quantity','Total_amount','date','updated_at')
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

class checkoutserializer(serializers.ModelSerializer):
    # carts = serializers.SerializerMethodField()
    # tag = CartSerializer(read_only=True, many=True)

    class Meta:
        model=checkout
        fields=("user","cart","Shipping_address",'No_of_items_to_checkout')
        
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
class orderserializer(serializers.ModelSerializer):
    class Meta:
        fields="__all__"
        model=Orders
        
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
        # response["coupon"]=instance.coupon.coupon
        # response["attributes"]=instance.attributes.Color
        return response


class bannerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Banner
class blogSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Blog


class faqSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("Question",)
        model = FAQ


class ffaqSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", 'Question', 'Answer', 'created_date', 'updated_at')
        model = FAQ


class ratingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("user", "product", "Reviews", "Rating")
        model = Rating
    #Rating=serializers.DecimalField(min_value=1,max_value=5, max_digits=3,decimal_places=1,)
    #user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def validate_Rating(self, value):
        if value == None:
            raise serializers.ValidationError("Please rate this product")
        return value
    # def validate_Reviews(self, value):
    #     if value =="":
    #         raise serializers.ValidationError("Please rate this product")
    #     return value

    def validate_product(self, value):
        if value == None:
            raise serializers.ValidationError("Please select the product")
        return value

    def validate_user(self, value):
        if value == None:
            raise serializers.ValidationError("user is required")
        return value
    # def validate(self, value):
    #     if value['Rating'] == None or value["Rating"]>5:
    #         raise serializers.ValidationError({"Rating": "please rate this product and maximum rating point is 5 star"})
    #     return value

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
            'gowdasandeep8105@gmail.com',
            ['sandeep.nexevo@gmail.com'],
            fail_silently=False,
        )
        return instance
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
                  'first_name', 'last_name', 'phone_no')
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs
    def validate_email(self, value):
        if value == None:
            raise serializers.ValidationError("Please provide email")
        return value
    def validate_first_name(self, value):
        if value == None:
            raise serializers.ValidationError("Please provide first name")
        return value
    def validate_last_name(self, value):
        if value == None:
            raise serializers.ValidationError("Please provide last name")
        return value
    def validate_phone_no(self, value):
        if value == None:
            raise serializers.ValidationError("Please provide phone number")
        return value 

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_no=validated_data['phone_no']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id','password')