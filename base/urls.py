from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('service/<id>/', views.service_detail, name='service_detail'),
    path('book-appointment/<service_id>/<doctor_id>/', views.book_appointment, name='book_appointment'),
    path('checkout/<billing_id>', views.checkout, name='checkout'),

]