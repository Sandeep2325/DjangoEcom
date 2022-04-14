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
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from django.core.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import update_last_login
# generating OTP


def generateOTP():
    global totp
    secret = pyotp.random_base32()
    # set interval(time of the otp expiration) according to your need in seconds.
    # global totp,one_time
    totp = pyotp.TOTP(secret, interval=300)
    one_time = totp.now()
    return one_time

# verifying OTP


def verifyOTP(one_time):
    answer = totp.verify(one_time)
    return answer


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def get(self, request):
        return Response({'Status': 'You cannot view all users data.....'})

    def post(self, request):
        email = request.data['email']
        print(email)

        data = User.objects.filter(email=email)
        print('data ', data)

        if data.exists():
            return Response({'msg': 'Already registered'}, status=status.HTTP_409_CONFLICT)
        else:
            serializer = self.serializer_class(data=request.data)
            print("ser", serializer)
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

                return Response(serializer.data, status=status.HTTP_201_CREATED)
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
            a=[]
            for i in User.objects.all():
                a.append(i.email)
            print(a)
            if email not in a:
                return Response({'msg': 'Email not registered'}, status=status.HTTP_404_NOT_FOUND)
            else:
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
            return Response({'msg': 'Not a valid request'}, status=status.HTTP_400_BAD_REQUEST)
class resendotp(APIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = (AllowAny,)  
    subject = 'Resent OTP'
    message = 'Resent OTP' + generateOTP()
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['']

    send_mail(
                subject,
                message,
                email_from,
                recipient_list,
                fail_silently=False,
            )
    
    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)
        
    #     # password2 = handler.hash()

    #     if serializer.is_valid():
    #         email = request.data['email']
    #         # password=request.data['password2']
    #         # password2 = handler.hash(password)
    #         # print(email)
    #         # User.objects.filter(email=email).update(password=password2)

    #         subject = 'Forgot Password OTP'
    #         message = 'Your password change OTP is ' + generateOTP()
    #         email_from = settings.EMAIL_HOST_USER
    #         recipient_list = [a]

    #         send_mail(
    #             subject,
    #             message,
    #             email_from,
    #             recipient_list,
    #             fail_silently=False,
    #         )
    #         return Response({'msg': 'sent'}, status=status.HTTP_200_OK)
    #     else:
    #         return Response({'msg': 'Not a valid request'}, status=status.HTTP_400_BAD_REQUEST)
      
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
        if one:
            User.objects.filter(email=email).update(
                password=password2, is_used=True, otp=one_time)
            return Response({'msg': 'Password changed succesfully'}, status=status.HTTP_200_OK)
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
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            user_id = valid_data['user']
            self.request.user = user_id
        except jwt.ExpiredSignatureError:
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

from rest_framework_simplejwt.tokens import RefreshToken
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
            return Response("Email is not Registered", status=status.HTTP_400_BAD_REQUEST)

        if val:
            if serializer.is_valid():
                user = authenticate(
                    username=request.data['email'], password=request.data['password'])
                update_last_login(None, user)
                # @classmethod
                # def get_token(cls, user):
                #     return RefreshToken.for_user(user)
                
                if user is not None and user.is_confirmed and user.is_active:  # change according to yourself
                    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
                    # payload = jwt_payload_handler(user)
                    # token1 = jwt.encode(payload, settings.SECRET_KEY)
                    
                    refresh1 = RefreshToken.for_user(user)
                    refresh_token=str(refresh1)
                    token2=str(refresh1.access_token)
                    print(refresh_token)
                    print(token2)
                    return Response({'msg': 'Login successful', 'is_confirmed': user.is_confirmed, 'access token': token2,"refresh token":refresh_token,
                                     }, status=status.HTTP_200_OK)
                else:
                    return Response({'msg': 'Account not approved or wrong Password.'}, status=status.HTTP_409_CONFLICT)
            else:
                return Response({'msg': 'Invalid data'}, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response({'Error': 'Not a valid user'}, status=status.HTTP_401_UNAUTHORIZED)
from rest_framework import generics
class ChangePasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer