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
from django.urls import path, include
from django.conf import settings  # add this
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views
from app1 import pdfviews
from app1 import views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenVerifyView
from django.conf.urls import handler404
import regex
from django.contrib.auth import views as auth_views
# handler404 = views.error_404_view
router = routers.DefaultRouter()
handler404 = views.handler404
urlpatterns = [

    #path('jet/', include('jet.urls', 'jet')),
    #path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    # path('admin/',views.countt),
    path('admin/', admin.site.urls),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
    #     template_name='main/password/password_reset_done.html'), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    #     template_name="main/password/password_reset_confirm.html"), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
    #     template_name='main/password/password_reset_complete.html'), name='password_reset_complete'),
    # path("password_reset", views.password_reset_request, name="password_reset"),
    #path('auth/', include('auth.urls')),
    #path('auth/', include('rest_auth.urls')),
    #path('registration/', include('rest_auth.registration.urls')),
    path('api/', include(router.urls)),
    #path('auth/', include('rest_auth.urls')),
    # path('',views.count),
    #path('baton/', include('baton.urls')),
    path('summernote/', include('django_summernote.urls')),
    # path('pdf/',pdfviews.GeneratePDF.as_view(),name="pdf"),
    path('', include('app1.urls')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    #path('', include(router.urls)),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#handler404 = 'app1.views.error_404_view'
