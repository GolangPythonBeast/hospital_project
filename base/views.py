from django.shortcuts import render, redirect
from base.models import Services, Appointment, Billing
from doctor.models import Doctor
from patient.models import Patient
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views import View
from django.http import JsonResponse
import requests

# Create your views here.
def index(request):
    services = Services.objects.all()
    appointments = Appointment.objects.all()

    context = {
        'services': services,
    }
    return render(request, 'index.html', context)

def service_detail(request, id):
    service = Services.objects.get(id=id)
    context = {
        'service': service,
    }
    return render(request, 'service-detail.html', context)

@login_required
def book_appointment(request, service_id, doctor_id):
    patient = Patient.objects.get(user=request.user)
    service = Services.objects.get(id=service_id)
    doctor = Doctor.objects.get(id=doctor_id)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        date_of_birth = request.POST.get('date_of_birth')
        issues = request.POST.get('issues')
        symptoms = request.POST.get('symptoms')

        # Update patient bio
        patient.full_name = full_name
        patient.email = email
        patient.mobile = mobile
        patient.gender = gender
        patient.address = address
        patient.date_of_birth = date_of_birth
        patient.save()

        # create appointment object
        appointment = Appointment.objects.create(
            service= service,
            doctor= doctor,
            patient= patient,
            appointment_date = doctor.next_available_appointment_date,
            issues=issues,
            symptoms=symptoms
        )

        # Create billing objects
        billing = Billing()
        billing.patient = patient
        billing.appointment = appointment
        billing.sub_total = appointment.service.cost
        billing.tax = appointment.service.cost * 5 / 100
        billing.total = billing.sub_total + billing.tax
        billing.status = "Unpaid"
        billing.save()
        return redirect('checkout', billing.billing_id)

    context = {
        'service': service,
        'doctor': doctor,
        'patient': patient,
    }
    return render(request, 'book-appointment.html', context)


@login_required
def checkout(request, billing_id):
    billing = Billing.objects.get(billing_id = billing_id)
    context = {
        'billing': billing,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
    }
    return render(request, 'checkout.html', context)


class PaystackPaymentView(View):
    def get(self, request):
        return render(request, 'payment_page.html', {
            'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY
        })

    def post(self, request):
        email = request.POST.get('email')
        amount = int(float(request.POST.get('amount')) * 100)  # Paystack uses kobo/cent

        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "email": email,
            "amount": amount,
            "callback_url": "http://yourdomain.com/verify-payment/",  # Your callback URL
        }

        response = requests.post(url, headers=headers, json=data)
        return JsonResponse(response.json())


# views.py
class VerifyPaymentView(View):
    def get(self, request, ref):
        url = f"https://api.paystack.co/transaction/verify/{ref}"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        }
        response = requests.get(url, headers=headers).json()

        if response['status']:
            # Successful payment logic
            return JsonResponse({"status": True, "data": response['data']})
        return JsonResponse({"status": False})


def verify_payment(request, reference):
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
    response = requests.get(url, headers=headers).json()

    if response['status'] and response['data']['status'] == 'success':
        # Payment was successful
        amount_paid = response['data']['amount'] / 100  # Convert back to dollars
        # Update your billing model here
        return render(request, 'payment_success.html')
    else:
        return render(request, 'payment_failed.html')