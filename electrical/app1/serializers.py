from dataclasses import field, fields
import email
from enum import unique
from genericpath import exists
from unittest.util import _MAX_LENGTH
from django.forms import CharField
from rest_framework import serializers
#from rest_auth.registration.serializers import RegisterSerializer
from . models import *
from math import ceil
from django.utils.timezone import now
from django.db import transaction
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
class CustomerAddressSerializers(serializers.ModelSerializer):
    class  Meta:
        fields = '__all__'
        model = Address
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())    
    #user=serializers.PrimaryKeyRelatedField(max_length=200)
    door_number=serializers.IntegerField()
    street=serializers.CharField(max_length=300)
    city=serializers.CharField(max_length=300)
    state=serializers.CharField(max_length=300)
    country=serializers.CharField(max_length=300)
    pincode=serializers.IntegerField()
    phone_no=serializers.IntegerField()
    def validate(self, attrs):
        if attrs['door_number'] in NULL:
            raise serializers.ValidationError({"door_number": "field required."})

        return attrs
    # def to_representation(self, instance):
    #     response=super().to_representation(instance)
    #     response["user"]=instance.user.username
    #     return response
class categorySerializer(serializers.ModelSerializer):
    class Meta:
        fields="__all__"
        model=Category
class productSerializer(serializers.ModelSerializer):
    #category_name = serializers.RelatedField(source='category.name', read_only=True)
    #category = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        fields=("id","title","sku","short_description","detail_description","image","product_image","price","discounted_price","category","is_active","created_at","updated_at","average_rating","count_review","reviews")
        model=Product
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['category'] = instance.category.brands
        #response['image'] = instance.image.last().image.url,instance.image.first().image.url,
        # response['price'] = instance.item.price
    
        return response
    def averagee_rating(self,instance):
        if Rating.objects.filter(Q(Status="Approved") & Q(product=instance)):
            review = Rating.objects.filter(Q(Status="Approved") & Q(product=instance)).aggregate(average=Avg('Rating'))
            avg=0
            
            if review["average"] is not None:
                avg=float(review["average"])
            #return avg
            if avg!=0:
                return "%.1f" %float(avg)
            else:
                return format_html("<p class=text-danger>No ratings yet!</p>")
        else:
            return format_html("<p class=text-danger>No ratings yet!</p>")
    def count_rating(self,instance):
        if Rating.objects.filter(Q(Status="Approved") & Q(product=instance)):
            reviews = Rating.objects.filter(Q(Status="Approved") & Q(product=instance)).aggregate(count=Count('id'))
            cnt=0
            if reviews["count"] is not None:
                cnt = int(reviews["count"])
            return cnt
    def reviewss(self,instance):
        if Rating.objects.filter(Q(Status="Approved") & Q(product=instance)):
            reviews=Rating.objects.filter(Q(Status="Approved") & Q(product=instance)).values_list("Reviews")
            for review in reviews:
                return review
        else:
            #return format_html("<p class=text-danger>No ratings yet!</p>")
            return "no ratings yet"
        
        # reviews=Rating.objects.filter(product=instance).values_list("Reviews")
        # for review in reviews:
        #     return review
        # reviews     
class productdetailserializer(serializers.ModelSerializer):
    class Meta:
        fields="__all__"
        model=Product
                
class attributesSerializer(serializers.ModelSerializer):
    class Meta:
        fields="__all__"
        model=Attributes
class ordersSerializer(serializers.ModelSerializer):
    class Meta:
        fields=("user","address","product",'quantity','coupon','attributes','status')
        model=Order
    def to_representation(self, instance):
        response=super().to_representation(instance)
        
        response["user"]=instance.user.username
        response["address"]=instance.address.city
        response["product"]=instance.product.title
        #response["coupon"]=instance.coupon.coupon
        #response["attributes"]=instance.attributes.Color
        return response
class bannerSerializer(serializers.ModelSerializer):
    class Meta:
        fields="__all__"
        model=Banner
class blogSerializer(serializers.ModelSerializer):
    class Meta:
        fields="__all__"
        model=Blog
class faqSerializer(serializers.ModelSerializer):
    class Meta:
        fields=("Question",)
        model=FAQ
class ffaqSerializer(serializers.ModelSerializer):
    class Meta:
        fields=("id",'Question','Answer','created_date','updated_at')
        model=FAQ    
class ratingSerializer(serializers.ModelSerializer):
    class Meta:
        fields=("user","product","Reviews","Rating")
        model=Rating
    Rating=serializers.DecimalField(min_value=1,max_value=5, max_digits=3,decimal_places=1,)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    # def validate(self, attrs):
    #     if attrs['user'] and attrs['product']:
    #         raise serializers.ValidationError({"user": "this user already rated this product"})
    #     return attrs    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user']=instance.user.username
        response["product"]="product: ",instance.product.title,"category: ",instance.product.category.brands
        
        return response
        
class customermessageSerializer(serializers.ModelSerializer):
    class Meta:
        fields="__all__"
        model=customer_message
    first_name=serializers.CharField(max_length=200)
    last_name=serializers.CharField(max_length=200)
    Email=serializers.EmailField(max_length=200)
    Phone=serializers.IntegerField()
    Message=serializers.CharField(max_length=500)
    
    def create(self, validate_data):
        instance = super(customermessageSerializer, self).create(validate_data)
        #return send_mail('Prakash Electrical',Message,'gowdasandeep8105@gmail.com',[email],fail_silently=False,),messages.success(request,"Successfully sent")
        send_mail(
            'You have message from one of your customer {}'.format(instance.first_name),
            'Here is the message. DATA: {}'.format(validate_data),
            'gowdasandeep8105@gmail.com',
            ['sandeep.nexevo@gmail.com'],
            fail_silently=False,
        )
        return instance
    
    def validate_first_name(self,value):
        if value is NULL:
            res= serializers.ValidationError('Enter First name')
            res.status_code = 200
            raise res 
        return value
class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"
#         model=customer_message
# class CouponSerializer(serializers.ModelSerializer):
#     """
#     RW Coupon serializer.
#     """

#     def validate(self, data):
#         """
        # Verify the input used to create or update the coupon is valid.  Because we don't support PATCH for the binding
        # field, we don't need to check self.instance for this.
#         """

#         # Verify if the expiration date is set that it's in the future.
#         if 'expires' in data:
#             if data['expires'] < now():
#                 raise serializers.ValidationError("Expiration date set in the past.")

#         # Verify if it's type is 'percentage' that the percentage value is set
#         # Verify if it's type is 'value' that the value is set.
#         if data['type'] == 'percent':
#             if 'value' in data and data['value'] > 1.0:
#                 raise serializers.ValidationError("Percentage discount specified greater than 100%.")

#         # Verify if it's bound, that the user exists or the email is valid.
#         """ if 'bound' in data and data['bound']:
#             if 'user' not in data:
#                 raise serializers.ValidationError("Bound to user, but user field not specified.") """

#         # Verify the lowercase code is unique.
#         # IntegrityError: UNIQUE constraint failed: coupons_coupon.code_l and not returning 400.
#         """ qs = Coupon.objects.filter(code_l=data['code'].lower())
#         if qs.count() > 0:
#             # there was a matching one, is it this one?
#             if self.instance:
#                 if data['code'].lower() != self.instance.code_l:
#                     raise serializers.ValidationError("Coupon code being updated to a code that already exists.")
#             else:
#                 raise serializers.ValidationError("Creating coupon with code that violates uniqueness constraint.")

#         data['code_l'] = data['code'].lower()

#         return data """

#     def validate_repeat(self, value):
#         """
#         Validate that if it's specified it can be -1, 1, or more than that, but not zero.
#         """

#         if value < 0:
#             raise serializers.ValidationError("Repeat field can be 0 for infinite, otherwise must be greater than 0.")
#         # if value > 6:
#         #     raise serializers.ValidationError("You Reached the maximum usage of Coupon")
#         # return value

#     def create(self, validated_data):
#         return Coupon.objects.create(**validated_data)

#     class Meta:
#         model = Coupon
#         fields = ('created', 'updated', 'code',
#                    'type', 'expires',
#                    'repeat','value', 'id')


# class ClaimedCouponSerializer(serializers.ModelSerializer):
#     """
#     RW ClaimedCoupon serializer.
#     """

#     def validate(self, data):
#         """
#         Verify the coupon can be redeemed.
#         """
#         coupon = data['coupon']
#         user = data['user']
#         # Is the coupon expired?
#         if coupon.expires and coupon.expires < now():
#             raise serializers.ValidationError("Coupon has expired.")
#         # Is the coupon bound to someone else?
#         """ if coupon.bound and coupon.user.id != user.id:
#             raise serializers.ValidationError("Coupon bound to another user.") """
#         # Is the coupon redeemed already beyond what's allowed?
#         redeemed = ClaimedCoupon.objects.filter(coupon=coupon.id, user=user.id).count()
#         if coupon.repeat > 0:   #change the repeat of coupon    
#             if redeemed >= coupon.repeat:
#                 # Already too many times (note: we don't update the claimed coupons, so this is a fine test).
#                 # Also, yes, > should never happen because the equals check will be hit first, but just in case
#                 # you somehow get beyond that... ;)
#                 raise serializers.ValidationError("Coupon has been used to its limit.")
#         return data
#     class Meta:
#         model = ClaimedCoupon
#         fields = ('redeemed', 'coupon', 'user', 'id')

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

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

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name','phone_no')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs
    def validate(self, attrs):
        if attrs['email'] is unique:
            raise serializers.ValidationError({"email": "This e-mail is already taken"})
        return attrs
    
    # def validate(self, attrs):
    #     if attrs['phone_no'] is unique & attrs['phone_no'] is NULL:
    #         raise serializers.ValidationError({"phone": "This phone mumber is already taken"})
    #     return attrs
    
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