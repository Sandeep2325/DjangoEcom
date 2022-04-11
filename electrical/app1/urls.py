from django.urls import path
from app1.models import Attributes
from rest_framework_simplejwt import views as jwt_views
from . import views
from app1.views import *
from app1.views1 import *
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('current-user/', CurrentUserViewSet.as_view(), name="current_user"),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('myaccount/',
         listmyaccount.as_view({'get': 'list'}), name="myaccount"),
    path('myaccount/create/', myaccountCreateView.as_view(),
         name='myaccount-create'),
    path('myaccount/<pk>/update/',
         myaccountupdateview.as_view(), name='myaccount-update'),
    path('categories/',
         listcategory.as_view({'get': 'list'}), name="category"),
    path('categories/<int:pk>/', detailcategory.as_view(), name="single_category"),
    path('brands/',
         listbrand.as_view({'get': 'list'}), name="Brands"),
    path('brands/<int:pk>/', detailbrand.as_view(), name="single_brand"),
    path('product/', Productlist.as_view({'get': 'list'}), name="product"),
    path('product/<int:pk>/', Productdetail.as_view(), name="single_product"),
    path('latest-product/', latestproductlist.as_view({'get': 'list'}), name="latest_product"),
    path('latest-product/<int:pk>/', latestproductdetail.as_view(), name="latestdetail_product"),
    path('mostselled-product/', mostselledproductlist.as_view({'get': 'list'}), name="mostselled_product"),
    path('mostselled-product/<int:pk>/', mostselledproductdetail.as_view(), name="mostselled_detail_product"),
    path('attributes/',
         attributelist.as_view({'get': 'list'}), name="attributes"),
    path('attributes/<int:pk>/', attributedetail.as_view(), name="single_attribute"),
#     path('order/', orderlist.as_view({'get': 'list'}), name="order"),
#     path('order/<int:pk>/', orderdetail.as_view(), name="single_order"),
#     path('order/create/', orderCreateView.as_view(), name='order-create'),
#     path('order/<pk>/delete/',orderDeleteView.as_view(), name='order-delete'),
    path('addresses/', AddressListView.as_view(), name='address-list'),
    path('addresses/create/', AddressCreateView.as_view(), name='address-create'),
    path('addresses/<pk>/update/',
         AddressUpdateView.as_view(), name='address-update'),
    path('addresses/<pk>/delete/',
         AddressDeleteView.as_view(), name='address-delete'),
    path('banner/', Listbanner.as_view({'get': 'list'}), name="banner"),
    path('blog/', Listblog.as_view({'get': 'list'}), name="blog"),
    path('faq/', Listfaq.as_view({'get': 'list'}), name="faq"),
    path('rating/', Listrating.as_view({'get': 'list'}), name="rating"),
    path('rating/create/', ratingCreateView.as_view(), name='rating-create'),
    path('rating/<pk>/update/', ratingupdateView.as_view(), name='rating-update'),
    path('customer-message/',listcustomermessage.as_view({'get': 'list'}), name="customer-message"),
    path('customer-message/create/', customermsgCreateView.as_view(),
         name='customer-message-create'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    #     path('cart1/',cart1.as_view(),name="cart1"),
    path('cart/', cartlist.as_view({'get': 'list'}), name="cart"),
    path('cart/<int:pk>/', cartdetail.as_view(), name="single_cart"),
    path('cart/create/', cartCreateView.as_view(), name='cart-create'),
    path('cart/<pk>/delete/',
         cartDeleteView.as_view(), name='cart-delete'),
    path('cart/<pk>/update/', cartupdateView.as_view(), name='cart-update'),
    path('checkout/', checkoutlist.as_view({'get': 'list'}), name="checkout"),
    path('checkout/create/', checkoutCreateView.as_view(), name='checkout-create'),
#     path('checkout-coupon/create/', checkoutcouponcreate.as_view(), name='checkoutcoupon-create'),
    path('orders/', orderslist.as_view({'get': 'list'}), name="orders"),
    path('orders/<int:pk>/', ordersdetail.as_view(), name="single_orders"),
    path('orders/create/', ordersCreateView.as_view(), name='orders-create'),
    path('orders/<pk>/delete/',
         ordersDeleteView.as_view(), name='orders-delete'),
    path('orders/<pk>/cancel/', ordercancelview.as_view(), name='order-cancel'),
    path('redeem_coupon/',couponredeemview.as_view(),name="coupon-redeem"),
    path('newsletter/', newsletterCreateView.as_view(),
         name='newscreate'),
    path('notification/', notificationlist.as_view({'get': 'list'}), name="notification"),
    path('notification/<pk>/delete/',
         deletenotification.as_view(), name='notification-delete'),
    path('unotification/', universalnotificationlist.as_view({'get': 'list'}), name="notification"),

    path('faq_enquiry/', enquiryCreateView.as_view(),
         name='faq_enquiry'),
    path('socialmedia/', socialmedialist.as_view({'get': 'list'}), name="social media"),
    
    
    
    path('register1', RegistrationAPIView.as_view()), #Registeration
    path('login1', LoginAPIView.as_view()), #Login after otp verification
    path('verify1', emailverify.as_view()), #otp Verify
    path('forgot1', ForgotPasswordView.as_view(), name='forgot-password'), #forgot Password
    path('reset1', ResetPasswordView.as_view(), name='reset-password'), #Resetting the Password after Login
    path('forgotverify1',forgotpasswordotpverification.as_view(),name='forgot-verify'),
]
