from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import  LoginForm, UserRegisterForm
from doctor import models as doctor_models
from patient import models as patient_models
from .models import User

from django.contrib.auth import authenticate, login, logout

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in!")
        return redirect('/')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            full_name = form.cleaned_data.get('full_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user_type = form.cleaned_data.get('user_type')

            user = authenticate(email=email, password=password)
            if user is not None:
                if user_type == 'Doctor':
                    doctor_models.Doctor.objects.create(user=user, full_name=full_name)
                elif user_type == 'Patient':
                    patient_models.Patient.objects.create(user=user, full_name=full_name, email=email)


                login(request, user)
                messages.success(request, "Account created successfully")
                return redirect('/')
            else:
                messages.error(request, 'Failed to register. Please try again')
    else:
        form = UserRegisterForm()

    context = {
        'form' : form,
    }
    return render(request, 'userauths/register.html', context)

def login_view(request):
    if request.user.is_authenticated:
        messages.success(request, 'You are already logged in')
        return redirect('/')

    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                user_instance = User.objects.get(email=email, is_active=True)
                user_authenticate = authenticate(request, email=email, password=password)
                if user_instance is not None:
                    login(request, user_authenticate)
                    messages.success(request, 'You are logged in successfully')
                    next_url = request.GET.get('next', '/')
                    return redirect(next_url) # this takes the user to intended page after login

                else:
                    messages.error(request, 'Username doesnt exist')
            except:
                messages.error(request, "User does not exist")

    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'userauths/login.html', context)


def logout_view(request):
    messages.success(request, "You have successfully logged out")
    logout(request)
    return redirect('sign-in')