from django.shortcuts import render, redirect
from flask import session

from base.models import Services, Appointment, Billing
from doctor.models import Doctor, Doctor_notification
from patient.models import Patient, Patient_notification
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views import View
from django.http import JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

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
        'flutterwave_public_key': settings.FLUTTERWAVE_PUBLIC_KEY,
    }
    return render(request, 'checkout.html', context)



def verify_paystack_payment(request, ref):
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }
    url = f"https://api.paystack.co/transaction/verify/{ref}"

    response = requests.get(url, headers=headers)
    res_data = response.json()

    if res_data['status'] and res_data['data']['status'] == 'success':
        amount = res_data['data']['amount'] / 100  # convert kobo to Naira
        email = res_data['data']['customer']['email']
        # ✅ Payment was successful
        # TODO: Update your database here
        billing_id = ref.split("-")[2]
        billing = Billing.objects.get(billing_id=billing_id)
        try:

            if billing.status == 'Unpaid':
                billing.status = 'Paid'
                billing.appointment.status = 'Completed'
                billing.save()

                Doctor_notification.objects.create(
                    doctor=billing.appointment.doctor,
                    appointment=billing.appointment,
                    type="New Appointment"
                )
                Patient_notification.objects.create(
                    patient=billing.appointment.patient,
                    appointment=billing.appointment,
                    type="Appointment Scheduled"
                )
                return render(request, 'success.html')

        except:
            return render(request, 'failed.html')

    else:
        return render(request, 'failed.html')







def verify_flutterwave_transaction(transaction_id):
    url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
    headers = {
        "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}"
    }
    response = requests.get(url, headers=headers)
    return response.json()


def payment_failed(request):
    return render(request, 'payment_failed.html')

