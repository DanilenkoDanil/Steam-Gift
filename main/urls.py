from django.urls import path
from . import views
from .views import DynamicStatusLoad


urlpatterns = [
    path('', views.head),
    path('account/', views.index),
    path('get_status/', DynamicStatusLoad.as_view(), name='load_status'),
    path('info/', views.handmade)
]
