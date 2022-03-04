"""electrical URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from xml.etree.ElementInclude import include
#from django.urls import url
from django.contrib import admin
from django.urls import path,include
from django.conf import settings #add this
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views  
from app1 import pdfviews
from app1 import views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenVerifyView
from django.conf.urls import handler404
import regex
#handler404 = 'app1.views.error_404_view'
router = routers.DefaultRouter()
urlpatterns = [
   
    #path('jet/', include('jet.urls', 'jet')),
    #path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    #path('auth/', include('rest_auth.urls')),
    #path('',views.count),
    #path('baton/', include('baton.urls')),
    path('summernote/', include('django_summernote.urls')),
    #path('pdf/',pdfviews.GeneratePDF.as_view(),name="pdf"),
    path('electrical/',include('app1.urls')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#handler404 = 'app1.views.error_404_view'