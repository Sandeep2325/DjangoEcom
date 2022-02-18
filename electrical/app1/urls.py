from django.urls import path
from app1.models import Attributes
from rest_framework_simplejwt import views as jwt_views
from . import views
from app1.views import Productdetail, Productlist, attributedetail, attributelist, detailcategory, listcategory, orderdetail, orderlist
urlpatterns=[
    path('categories',views.listcategory.as_view({'get': 'list'}),name="category"),
    path('categories/<int:pk>/',detailcategory.as_view(),name="single_category"),

    path('product',Productlist.as_view({'get':'list'}),name="product"),
    path('product/<int:pk>/',Productdetail.as_view(),name="single_product"), 

    path('attributes',attributelist.as_view({'get':'list'}),name="attributes"),
    path('attributes/<int:pk>/',attributedetail.as_view(),name="single_attribute"),

    path('order',orderlist.as_view({'get':'list'}),name="order"),
    path('order/<int:pk>/',orderdetail.as_view(),name="single_order"), 
 ]