from django.urls import path,include
from app1.models import Attributes
from rest_framework_simplejwt import views as jwt_views
from . import dummyview
from app1.views import *
from app1.views1 import *
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings 
from . import payment
router = routers.DefaultRouter()
router.register('products-brand', productview)
# router.register('productbrand',product_brand,basename="brand")
router.register('products-category',most_categoryview,basename="products-category")
router.register('latest-product', latestview,basename="latest-product")
router.register("blogg",blogview)
#filter
#search functionality filters
router.register('search-high-to-low',searchproductHitoLo,basename="search-high-to-low")
router.register('search-low-to-high',searchproductLotoHi,basename="search-low-to-high")
router.register('search-newest',searchnewest,basename="search-newest")
router.register('search-discount',searchdiscount,basename="search-discount")
#faq page
router.register('faq',Listfaq)
router.register('enquirycreate',enquirycreate)
router.register('myaccountcreate',myaccountCreateView)
router.register('userphotocreate',userphotocreate)
router.register('cartCreateView1',cartCreateView1)
# router.register('invoice',invoice)
router.register('userphoto1',userphoto1,basename="userphoto1")
router.register('addresscreate',AddressCreateView)
router.register("listsubcategory",subcategoryview)
router.register('newsletter',newsletterCreateView)
router.register('products',productsearch)
# router.register('sidebarfilter1',sidebarfilterview)
router.register('addresses',addresslist)
router.register('defaultaddressget',defaultaddressget)
router.register("listattributes",listattributes)
router.register("brands",listbrand)
# router.register('notification',notificationlist,basename="notification")
router.register('unotification',universalnotificationlist,basename="unotification")
app_name = 'Product'
urlpatterns = [
     path('pay/', payment.start_payment, name="payment"),
    path('payment/success/', payment.handle_payment_success, name="payment_success"),
    path('getSubcategory/', get_subcategory),
    path('dashboard',dashboard),
    path('', include(router.urls)),
    path('current-user/', CurrentUserViewSet.as_view(), name="current_user"),
#     path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('register/', RegisterView.as_view(), name='auth_register'),

    path('myaccount/',
         listmyaccount.as_view({'get': 'list'}), name="myaccount"),
    path('myaccount/update/<pk>',
         myaccountupdateview.as_view(), name='myaccount-update'),
    path('myaccountemail/',myaccountemail.as_view(),name="myaccountemail"),
    path('myaccountemailverify/',myaccountemailverify.as_view(),name="myaccountemailverify"),
    
    path('userphoto/<pk>',
         userphoto11.as_view(), name='userphoto'),
    path('categories/',
         listcategory.as_view({'get': 'list'}), name="category"),
    path('categories/<int:pk>/', detailcategory.as_view(), name="single_category"),
    path('brands1/', brandproductlist1.as_view(), name='brand1'),
    path('brand/', brandproductlist.as_view({'get': 'list'}), name="brand_product"),
    path('product/', Productlist.as_view({'get': 'list'}), name="product"),
    path('product_brand/<int:pk>/',product_brand.as_view({'get': 'list'}),name="product_brand"),
    path('product/<int:pk>/', Productdetail.as_view(), name="single_product"),
    
#     path('newest/', newest.as_view({'get': 'list'}), name="newset"),
#     path('latest-product/', latestproductlist.as_view({'get': 'list'}), name="latest_product"),
#     path('latest-product/<int:pk>/', latestproductdetail.as_view(), name="latestdetail_product"),

    path('mostselled-product/', mostselledproductlist.as_view({'get': 'list'}), name="mostselled_product"),
    path('mostselled-product/<int:pk>/', mostselledproductdetail.as_view(), name="mostselled_detail_product"),
    path('attributes/',
         attributelist.as_view({'get': 'list'}), name="attributes"),
#     path('attributes/<int:pk>/', attributedetail.as_view(), name="single_attribute"),
#     path('addresses/create/', AddressCreateView1.as_view(), name='address-create'),
    path('addresses/update/<pk>',
         AddressUpdateView.as_view(), name='address-update'),
    path('defaddress/update/<pk>',
         defaultaddress.as_view(), name='deafult-address'),
    path('addresses/<pk>/delete/',
         AddressDeleteView.as_view(), name='address-delete'),
    path('banner/', Listbanner.as_view({'get': 'list'}), name="banner"),
    path('blog/', Listblog.as_view({'get': 'list'}), name="blog"),
    path('blog/<int:pk>/', blogdetail.as_view(), name="single_blog"),
    path('rating/', Listrating.as_view({'get': 'list'}), name="rating"),
    path('rating/create/', ratingCreateView.as_view(), name='rating-create'),
    path('rating/update/<pk>', ratingupdateView.as_view(), name='rating-update'),
   
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    #     path('cart1/',cart1.as_view(),name="cart1"),
    path('cart/', cartlist.as_view({'get': 'list'}), name="cart"),
    path('cart/<int:pk>/', cartdetail.as_view(), name="single_cart"),
    path('cart/<pk>/delete/',
         cartDeleteView.as_view(), name='cart-delete'),
    path('cartquantity/update/<pk>', cartquantityupdateView.as_view(), name='cart-update'),
    path('ordersummary',ordersummaryview.as_view(),name="ordersummary"),
    path('checkoutsummary',checkoutsummaryview.as_view(),name="checkoutsummary"),
#     path('notification/', notificationlist.as_view({'get': 'list'}), name="notification"),
    path('notification/<pk>/delete/',
         deletenotification.as_view(), name='notification-delete'),
#     path('unotification/', universalnotificationlist.as_view({'get': 'list'}), name="notification"),

    path('invoice/', invoice.as_view(),name="invoice"),
    #filters
    path('filters/', filters.as_view(),name="filters"),
#     path('hightolow/', hightolow.as_view(),name="hightolow"),
#     path('lowtohigh/', lowtohigh.as_view(),name="lowtohigh"),
#     path('newest/', newest.as_view(),name="newest"),
#     path('discount/', discount.as_view(),name="discount"),
#     path('sidebarfilter/', sidebarfilterview.as_view(),name="side-bar-filter"),
    path('socialmedia/', socialmedialist.as_view({'get': 'list'}), name="social media"),
    path('register1/', RegistrationAPIView.as_view(),name="register"), #Registration
    path('login1/', LoginAPIView.as_view(),name="login"), #Login after otp verification
    path('verify1/', emailverify.as_view(),name="verify"), #otp Verify
    path('forgot1/', ForgotPasswordView.as_view(), name='forgot-password'), #forgot Password
    path('resend1/', resend.as_view(), name='resend'),
    path('accountverify1/', accountverifyview.as_view(), name='resend'),
    path('reset1/', ResetPasswordView.as_view(), name='reset-password'), #Resetting the Password after Login
    path('forgotverify1/',forgotpasswordotpverification.as_view(),name='forgot-verify'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
