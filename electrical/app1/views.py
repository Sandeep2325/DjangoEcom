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
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.mixins import ListModelMixin
from django.http import Http404
from rest_framework.viewsets import ViewSet
from rest_framework import generics
from . serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import viewsets,filters, status
from django.shortcuts import get_object_or_404
from rest_framework.generics import (ListAPIView, RetrieveAPIView, CreateAPIView,UpdateAPIView, DestroyAPIView,GenericAPIView)
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
    usercount=User.objects.all().count()
    productcount=Product.objects.all().count()
    ordercount=Order.objects.all().count()
    context={'usercount':usercount,
             'productcount':productcount,
             'ordercount':ordercount}
    return render(request,"templates/admin/index.html",context)
##############################################################################################################################################
class listcategory(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class=categorySerializer

class detailcategory(generics.RetrieveUpdateDestroyAPIView):
    queryset=Category.objects.all()
    #serializer_class=categorySerializer
    def list(self, request):
        serializer = categorySerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = categorySerializer(item)
        return Response(serializer.data)
    
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
    queryset = Product.objects.all()
    # product_detail = Product.objects.get(id=id)
    # review = Rating.objects.filter(product = product_detail)
    serializer_class=productSerializer
    pagination_class = PageNumberPagination
    
     
class Productdetail(generics.RetrieveAPIView):
    queryset=Product.objects.all()
    serializer_class=productSerializer
class attributelist(viewsets.ModelViewSet):
    queryset = Attributes.objects.all()
    def list(self, request):
        serializer = attributesSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = attributesSerializer(item)
        return Response(serializer.data)

class attributedetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Attributes.objects.all()
    serializer_class=attributesSerializer

class orderlist(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    def list(self, request):
        serializer = ordersSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = ordersSerializer(item)
        return Response(serializer.data)

##################################################################################
""" class OrderDetailView(RetrieveAPIView):
    serializer_class = ordersSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            order = Order.objects.all()
            return order
        except ObjectDoesNotExist:
            raise Http404("You do not have an active order") """
#########################################################################################
class orderdetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Order.objects.all()
    serializer_class=ordersSerializer

class orderCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ordersSerializer
    queryset = Order.objects.all()

############################################################################################
class AddressListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CustomerAddressSerializers

    def get_queryset(self):
        address_type = self.request.query_params.get('address_type', None)
        qs = Address.objects.all()
        if address_type is None:
            return qs
        return qs.filter(user=self.request.user, address_type=address_type)


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

#######################################################################################################
""" class ListCustomerAddress(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = CustomerAddressSerializers """

class Listbanner(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = bannerSerializer

class Listblog(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = blogSerializer
class Listfaq(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = ffaqSerializer
class faqCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = faqSerializer
    queryset = FAQ.objects.all()
class Listrating(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = ratingSerializer
class ratingCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ratingSerializer
    queryset = Rating.objects.all()
class ratingupdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ratingSerializer
    queryset = Rating.objects.all()
    
    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.name = request.data.get("Rating")
    #     instance.save()
    #     serializer = self.get_serializer(instance)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)
    
class listcustomermessage(viewsets.ModelViewSet):
    queryset=customer_message.objects.all()
    serializer_class=customermessageSerializer
""" class customermsgCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = customermessageSerializer
    queryset = Address.objects.all() """
class customermsgCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = customermessageSerializer
    queryset = customer_message.objects.all()

class AddCouponView(APIView):
    def post(self, request, *args, **kwargs):
        code = request.data.get('code', None)
        if code is None:
            return Response({"message": "Invalid data received"}, status=HTTP_400_BAD_REQUEST)
        order = Order.objects.get(
            user=self.request.user, ordered=False)
        coupon = get_object_or_404(Coupon, code=code)
        order.coupon = coupon
        order.save()
        return Response(status=HTTP_200_OK)


# def group_required(api_command):
#     """
#     This is implemented such that it's default open.
#     """

#     def in_groups(u):
#         if u.is_authenticated():
#             # supervisor can do anything
#             if u.is_superuser:
#                 return True

#             # coupons have permissions set (I think I may set them by default to remove this check)
#             if settings.COUPON_PERMISSIONS and api_command in settings.COUPON_PERMISSIONS:
#                 group_names = settings.COUPON_PERMISSIONS[api_command]

#                 # but no group specified, so anyone can.
#                 if len(group_names) == 0:
#                     return True

#                 # group specified, so only those in the group can.
#                 if bool(u.groups.filter(name__in=group_names)):
#                     return True
#         return False
#     return user_passes_test(in_groups)


# def get_redeemed_queryset(user, coupon_id=None):
#     """
#     Return a consistent list of the redeemed list.  across the two endpoints.
#     """

#     api_command = 'REDEEMED'

#     # If the a coupon isn't specified, get them all.
#     if coupon_id is None:
#         qs_all = ClaimedCoupon.objects.all()
#         qs_some = ClaimedCoupon.objects.filter(user=user.id)
#     else:
#         qs_all = ClaimedCoupon.objects.filter(coupon=coupon_id)
#         qs_some = ClaimedCoupon.objects.filter(coupon=coupon_id, user=user.id)

#     if user.is_superuser:
#         return qs_all

#     if settings.COUPON_PERMISSIONS and api_command in settings.COUPON_PERMISSIONS:
#         group_names = settings.COUPON_PERMISSIONS[api_command]

#         # So the setting is left empty, so default behavior.
#         if len(group_names) == 0:
#             return qs_some

#         # group specified, so only those in the group can.
#         if bool(user.groups.filter(name__in=group_names)):
#             return qs_all

#     return qs_some


# class CouponViewSet(viewsets.ModelViewSet):
   

#     filter_backends = (filters.SearchFilter, DjangoFilterBackend)
#     filter_class = CouponFilter
#     search_fields = ('code',)
#     serializer_class = CouponSerializer

#     def get_queryset(self):
#         """
#         Return a subset of coupons or all coupons depending on who is asking.
#         """

#         api_command = 'LIST'
#         qs_all = Coupon.objects.all()
#         #qs_some = Coupon.objects.filter(user=self.request.user.id)

#         if self.request.user.is_superuser:
#             return qs_all

#         # This is different from the normal check because it's default closed.
#         if settings.COUPON_PERMISSIONS and api_command in settings.COUPON_PERMISSIONS:
#             group_names = settings.COUPON_PERMISSIONS[api_command]

#             # So the setting is left empty, so default behavior.
#             """ if len(group_names) == 0:
#                 return qs_some """

#             # group specified, so only those in the group can.
#             if bool(self.request.user.groups.filter(name__in=group_names)):
#                 return qs_all

#         return qs_all

#     @method_decorator(group_required('CREATE'))
#     def create(self, request, **kwargs):
#         """
#         Create a coupon
#         """

#         serializer = CouponSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @method_decorator(group_required('DELETE'))
#     def destroy(self, request, pk=None, **kwargs):
#         """
#         Delete the coupon.
#         """

#         coupon = get_object_or_404(Coupon.objects.all(), pk=pk)
#         coupon.delete()

#         return Response(status=status.HTTP_204_NO_CONTENT)

#     def partial_update(self, request, pk=None, **kwargs):
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     def retrieve(self, request, pk=None, **kwargs):
#         """
#         Anybody can retrieve any coupon.
#         """

#         value_is_int = False

#         try:
#             pk = int(pk)
#             value_is_int = True
#         except ValueError:
#             pass

#         if value_is_int:
#             coupon = get_object_or_404(Coupon.objects.all(), pk=pk)
#         else:
#             coupon = get_object_or_404(Coupon.objects.all(), code_l=pk.lower())

#         serializer = CouponSerializer(coupon, context={'request': request})

#         return Response(serializer.data)

#     @method_decorator(group_required('UPDATE'))
#     def update(self, request, pk=None, **kwargs):
#         """
#         This forces it to return a 202 upon success instead of 200.
#         """

#         coupon = get_object_or_404(Coupon.objects.all(), pk=pk)

#         serializer = CouponSerializer(coupon, data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     #@detail_route(methods=['get'])
#     def redeemed(self, request, pk=None, **kwargs):
#         """
#         Convenience endpoint for getting list of claimed instances for a coupon.
#         """

#         coupon = get_object_or_404(Coupon.objects.all(), pk=pk)
#         qs = get_redeemed_queryset(self.request.user, coupon.id)

#         serializer = ClaimedCouponSerializer(qs, many=True, context={'request': request})

#         return Response(serializer.data)

#     #@detail_route(methods=['put'])
#     def redeem(self, request, pk=None, **kwargs):
#         """
#         Convenience endpoint for redeeming.
#         """

#         queryset = Coupon.objects.all()
#         coupon = get_object_or_404(queryset, pk=pk)

#         # Maybe should do coupon.redeem(user).
#         # if data['expires'] < now():
        
#         data = {
#             'coupon': pk,
#             'user':   self.request.user.id,
#         }

#         serializer = ClaimedCouponSerializer(data=data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()

#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ClaimedCouponViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that lets you retrieve claimed coupon details.
#     """

#     filter_backends = (DjangoFilterBackend,)
#     filter_fields = ('user',)
#     serializer_class = ClaimedCouponSerializer

#     def get_queryset(self):
#         return get_redeemed_queryset(self.request.user)

#     def create(self, request, **kwargs):
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     @method_decorator(group_required('DELETE'))
#     def destroy(self, request, pk=None, **kwargs):
#         """
#         Basically un-redeem a coupon.
#         """

#         redeemed = get_object_or_404(ClaimedCoupon.objects.all(), pk=pk)
#         redeemed.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        
#     def partial_update(self, request, pk=None, **kwargs):
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     def retrieve(self, request, pk=None, **kwargs):
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     def update(self, request, pk=None, **kwargs):
#         return Response(status=status.HTTP_404_NOT_FOUND)
