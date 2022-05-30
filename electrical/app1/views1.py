from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import pyotp
import random
import jwt
import hashlib
from django.conf import settings
from django.core.mail import send_mail
from .models import User
from .serializers1 import LoginSerializer, RegistrationSerializer, VerifyOTPSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from .serializers1 import *
from django.contrib.auth import authenticate
from passlib.hash import django_bcrypt_sha256 as handler
# from passlib.hash import django_pbkdf2_sha256 as handler
# from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from django.core.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.db.models.query_utils import Q
from rest_framework import generics
from rest_framework import permissions
from django.shortcuts import render
# generating OTP
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
class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    # def get(self, request):
    #     return Response({'Status': 'You cannot view all users data.....'})
    def post(self, request):
        email = request.data['email']
        phone_no=request.data['phone_no']
        data = User.objects.filter(Q(email=email)& Q(is_confirmed=True))
        data1=User.objects.filter(phone_no=phone_no)
        if data1.exists():
            return Response ({'msg':"Phone number already exists"},status=status.HTTP_409_CONFLICT)
        if data.exists():
            return Response({'msg': 'Already registered'}, status=status.HTTP_409_CONFLICT)
        else:
            serializer = self.serializer_class(data=request.data)
            #print("ser", serializer)
            name = request.data['username']
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = f'Welcome {name} Your OTP is : ' + \
                    generateOTP()
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                message = message
                subject = "OTP" 
                send_mail(
                    subject,
                    message,
                    email_from,
                    recipient_list,
                    fail_silently=False,
                )
                return Response({'msg':"OTP sent to your Email"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"Error": "Sign Up Failed"}, status=status.HTTP_400_BAD_REQUEST)
            
class VerifyOTPView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifyOTPSerializer
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        email = request.data['email']
        one_time = request.data['otp']
        print('one_time_password', one_time)
        one = verifyOTP(one_time)
        print('one', one)
        if one:
            User.objects.filter(email=email).update(
                is_confirmed=True, is_used=True, otp=one_time)
            return Response({'msg': 'OTP verfication successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'OTP verfication Failed'}, status=status.HTTP_400_BAD_REQUEST)

# it will send the mail with changed password which is generated randomly
class emailverify(APIView):
    permission_classes = (AllowAny,)
    serializer_class = emailverification
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        email = request.data['email']
        one_time = request.data['otp']
        # password=request.data['password2']
        # password2 = handler.hash(password)
        print('one_time_password', one_time)
        one = verifyOTP(one_time)
        print('one', one)
        if one:
            User.objects.filter(email=email).update(
                is_confirmed=True, is_used=True, otp=one_time)
            return Response({'msg': 'OTP verfication successful and Account created'}, status=status.HTTP_200_OK)
        else: 
            return Response({'msg': 'OTP verfication Failed'}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        # password2 = handler.hash()
         
        if serializer.is_valid():
            email = request.data['email']
            # password=request.data['password2']
            # password2 = handler.hash(password)
            # print(email)
            # User.objects.filter(email=email).update(password=password2)
            # a=[]
            data= User.objects.filter(email=email)
                # a.append(i.email)
            if data.exists():
                subject = 'Forgot Password OTP'
                message = 'Your password change OTP is ' + generateOTP()
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]

                send_mail(
                    subject,
                    message,
                    email_from,
                    recipient_list,
                    fail_silently=False,
                    )
                return Response({'msg': 'sent'}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Email not registered'}, status=status.HTTP_404_NOT_FOUND)
                
        else:
            return Response({'msg': 'Not a valid request'}, status=status.HTTP_400_BAD_REQUEST)
   
from hashlib import sha1     
class forgotpasswordotpverification(APIView):
    permission_classes = (AllowAny,)
    serializer_class = forgotverifyserializer

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        email = request.data['email']
        one_time = request.data['otp']
        password=request.data['password2']
        password2 = handler.hash(password)
        print('one_time_password', one_time)
        one = verifyOTP(one_time)
        print('one', one)
        data = User.objects.filter(Q(email=email)& Q(is_confirmed=True))
        # print("-----present password-----",present_password)
        # print("-----entered password-----",password2)
        if one:
            if data.exists():
                User.objects.filter(email=email).update(
                    password=password2, is_used=True, otp=one_time)
                return Response({'msg': 'Password changed succesfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'msg':'Entered Email id is not registered'},status=status.HTTP_409_CONFLICT)
        else:
            return Response({'msg': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = (AllowAny,)
    def post(self, request):
        token1 = request.META["HTTP_AUTHORIZATION"]
        token = token1.split(' ')[1]
        data = {'token': token}
        payload_decoded = jwt.decode(token, settings.SECRET_KEY)
        try:
            # valid_data = VerifyJSONWebTokenSerializer().validate(data)
            valid_data=""
            user_id = valid_data['user']
            self.request.user = user_id
        except :
            return Response(status=440)
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            new_password = request.data['new_password']
            confirm_password = request.data['confirm_password']
            if new_password == confirm_password:
                password = handler.hash(new_password)
                email = request.data['email']
                User.objects.filter(
                    email=email, user_id=user_id).update(password=password)

                return Response({'msg': 'Password updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'New Password and Confirm Password does not match, please enter again'}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({'msg': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        print('email', email)
        filter_data = User.objects.filter(email=email).values('is_active')
        print('filter_data', filter_data)
        if filter_data.exists():
            val = filter_data[0]['is_active']
        else:
            return Response({"msg":"Email is not Registered"}, status=status.HTTP_400_BAD_REQUEST)
        if val:
            if serializer.is_valid():
                user = authenticate(
                    username=request.data['email'], password=request.data['password'])
               
                if user is not None and user.is_confirmed and user.is_active:  # change according to yourself
                    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
                    payload = jwt_payload_handler(user)
                    token1 = jwt.encode(payload, settings.SECRET_KEY)
                    refresh1 = RefreshToken.for_user(user)
                    refresh_token=str(refresh1)
                    token2=str(refresh1.access_token)
                    token3=AccessToken.for_user(user)
                    print("......",token3)
                    print("......",token2)
                    # token2=str(AccessToken.for_user(user))
                    # print(refresh_token)
                    # print(token2)
                    # print(token1)
                    return Response({'msg': 'Login successful', 'is_confirmed': user.is_confirmed, 'access token': token2,"refresh token":refresh_token,
                                     }, status=status.HTTP_200_OK)
                
                else:
                    return Response({'msg': 'Invalid credentials'}, status=status.HTTP_409_CONFLICT)
            else:
                return Response({'msg': 'Invalid data'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'Error': 'Not a valid user'}, status=status.HTTP_401_UNAUTHORIZED)

class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    
class resend(APIView):
    serializer_class = resendserializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        # password2 = handler.hash()
         
        if serializer.is_valid():
            email = request.data['email']
            data= User.objects.filter(email=email)
            if data.exists():
                subject = 'Resend OTP'
                message = 'Your resend OTP ' + generateOTP()
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]

                send_mail(
                    subject,
                    message,
                    email_from,
                    recipient_list,
                    fail_silently=False,
                    )
                return Response({'msg': 'sent'}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Email not registered'}, status=status.HTTP_404_NOT_FOUND)
                
        else:
            return Response({'msg': 'Not a valid request'}, status=status.HTTP_400_BAD_REQUEST)
# from common.helper import CommonHelper

# class Resent1(generics.CreateAPIView):
#     """
#     Resent OTP
#     """
#     # model = models.User
#     permission_classes = (permissions.AllowAny,)
#     serializer_class =ResentSerializer

#     def post(self, request, *args, **kwargs):
#         """
#         Resent OTP on mail and email. OTP valid for 15 min only.
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         serializer = self.get_serializer(data=request.data)
#         if not serializer.is_valid():
#             raise serializers.ValidationError(serializer.errors, code=status.HTTP_200_OK)
#         try:
#             kwargs = User.email(serializer.initial_data["device"])
#             user = User.email_exists(**kwargs)
#             if not user:
#                 return Response(render(False, None, "User not exists", status.HTTP_200_OK))
#             user.verification.generate_otp()
#             message = f"Verification OTP sent to {user.mobile} and {user.email}"
#         except Exception as ex:
#             return Response(render(False, None, ex.args, status.HTTP_200_OK))
#         return Response(render(True, None, message, status.HTTP_201_CREATED))