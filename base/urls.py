from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('service/<>', views.service_detail, name='service'),
]