from django.urls import path

from . import views

urlpatterns = [
    path('sign-up/', views.register, name='sign-up'),
    path('sign-in/', views.login_view, name='sign-in'),
    path('sign-out/', views.logout_view, name='sign-out'),
]