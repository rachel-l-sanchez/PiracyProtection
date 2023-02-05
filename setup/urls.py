from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from piracyApp import views 
import os
from pathlib import Path
from piracyApp.views import StripeWebhookView
from django.views.generic import TemplateView
from piracyApp.views import CancelView


BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = '/uploads/'

MEDIA_ROOT= os.path.join(BASE_DIR, 'piracyApp/uploads')

urlpatterns = [
    path('edit/<int:id>/', views.upload_file, name="upload"),
    path('', views.register, name='register'), 
    path('landing/', views.HomePageView.as_view(), name='landing'),
    path(r'create/', views.create, name='create'),
    path('charge/', views.charge, name='charge'), 
    path('login/', views.loginWithSerialKey,name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('valid/', views.view, name='view'),
    path('admin/', admin.site.urls),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('webhooks/stripe/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path('success/', views.homepage, name='homepage'),
    path('delete/<id>/', views.delete, name='delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
       
app_name = "main"   