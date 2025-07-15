from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('service/<id>/', views.service_detail, name='service_detail'),
    path('book-appointment/<service_id>/<doctor_id>/', views.book_appointment, name='book_appointment'),
    path('checkout/<billing_id>', views.checkout, name='checkout'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
    path('verify-payment/<str:ref>/', views.verify_paystack_payment, name='verify-paystack-payment'),
    path('verify-flutterwave/<payment_id>', views.verify_flutterwave_transaction, name='verify_payment'),

]