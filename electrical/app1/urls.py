from django.urls import path
from app1.models import Attributes
from rest_framework_simplejwt import views as jwt_views
from . import views
from app1.views import *

urlpatterns=[
     
    path('categories/',views.listcategory.as_view({'get': 'list'}),name="category"),
    path('categories/<int:pk>/',detailcategory.as_view(),name="single_category"),
    path('product/',Productlist.as_view({'get': 'list'}),name="product"),
    path('product/<int:pk>/',Productdetail.as_view(),name="single_product"), 
    path('attributes/',attributelist.as_view({'get':'list'}),name="attributes"),
    path('attributes/<int:pk>/',attributedetail.as_view(),name="single_attribute"),
    path('order/',orderlist.as_view({'get':'list'}),name="order"),
    path('order/<int:pk>/',orderdetail.as_view(),name="single_order"),
    path('order/create/', orderCreateView.as_view(), name='order-create'),
    path('addresses/',AddressListView.as_view(), name='address-list'),
    path('addresses/create/', AddressCreateView.as_view(), name='address-create'),
    path('addresses/<pk>/update/',
         AddressUpdateView.as_view(),name='address-update'),
    path('addresses/<pk>/delete/',
         AddressDeleteView.as_view(),name='address-delete'),
    path('banner/',Listbanner.as_view({'get':'list'}),name="banner"),
    path('blog/',Listblog.as_view({'get':'list'}),name="blog"),
    path('faq/',Listfaq.as_view({'get':'list'}),name="faq"),
    path('faq/create/', faqCreateView.as_view(), name='faq-create'),
    path('rating/',Listrating.as_view({'get':'list'}),name="rating"),
    path('rating/create/', ratingCreateView.as_view(), name='rating-create'),
    path('rating/<pk>/update/', ratingupdateView.as_view(), name='rating-update'),
    path('customer-message/',listcustomermessage.as_view({'get':'list'}),name="customer-message"),
    path('customer-message/create/',customermsgCreateView.as_view(), name='customer-message-create'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
 ]