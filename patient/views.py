from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models

from base import models as base_models
from patient import models as patient_models
from doctor import models as doctor_models
from datetime import datetime
from django.utils import timezone

@login_required
def dashboard(request):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(patient=patient)
    notifications = patient_models.Patient_notification.objects.filter(patient=patient, seen=False)
    
    total_spent = base_models.Billing.objects.filter(patient=patient).aggregate(total_spent= models.Sum('total'))['total_spent']
    
    context = {
        'appointments': appointments,
        'notifications': notifications,
        'total_spent': total_spent,
    }
    return render(request, 'patient/dashboard.html', context)

@login_required
def appointments(request):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(patient=patient)
    context = {
        'appointments': appointments,
    }
    return render(request, 'patient/appointments.html', context)


@login_required
def appointment_detail(request, appointment_id):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, patient=patient)
    medical_records = base_models.MedicalRecord.objects.filter(appointment=appointment)
    lab_tests = base_models.Labtest.objects.filter(appointment=appointment)
    prescriptions = base_models.Prescription.objects.filter(appointment=appointment)

    context = {
        'appointment': appointment,
        'medical_records': medical_records,
        'lab_tests': lab_tests,
        'prescriptions': prescriptions,
    }
    return render(request, 'patient/appointment_detail.html', context)

@login_required
def activate_appointment(request, appointment_id):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, patient=patient)
    appointment.status = 'Scheduled'
    appointment.save()
    
    messages.success(request, "Appointment Resheduled successfully")
    return redirect('patient:appointment_detail', appointment.appointment_id)


@login_required
def complete_appointment(request, appointment_id):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, patient=patient)
    appointment.status = 'Completed'
    appointment.save()
    
    messages.success(request, "Appointment Completed successfully")
    return redirect('patient:appointment_detail', appointment.appointment_id)


@login_required
def cancel_appointment(request, appointment_id):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, patient=patient)
    appointment.status = 'Cancelled'
    appointment.save()
    
    messages.success(request, "Appointment cancelled successfully")
    return redirect('patient:appointment_detail', appointment.appointment_id)


@login_required
def activate_appointment(request, appointment_id):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, patient=patient)
    appointment.status = 'Scheduled'
    appointment.save()
    
    messages.success(request, "Appointment Resheduled successfully")
    return redirect('patient:appointment_detail', appointment.appointment_id)

@login_required
def complete_appointment(request, appointment_id):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, patient=patient)
    appointment.status = 'Completed'
    appointment.save()
    
    messages.success(request, "Appointment Completed successfully")
    return redirect('patient:appointment_detail', appointment.appointment_id)




@login_required
def payments(request):
    patient = patient_models.Patient.objects.get(user=request.user)
    payments = base_models.Billing.objects.filter(patient=patient, status='Paid') # filter is used to get more values of payments in a list
    
    context = {
        'payments': payments,
    }
    return render(request, 'patient/payments.html', context)

@login_required
def notification(request):
    patient = patient_models.Patient.objects.get(user=request.user)
    notifications = patient_models.Patient_notification.objects.filter(patient=patient, seen=False)
    
    context = {
        'notifications': notifications
    }
    return render(request, 'patient/notifications.html', context)

@login_required
def make_notification(request, id):
    patient = patient_models.Patient.objects.get(user=request.user)
    notification = patient_models.Patient_notification.objects.get(patient=patient, id=id)
    notification.seen = True
    notification.save()
    
    messages.success(request, 'Notication Seen Successfully')
    return redirect('patient:notification')


@login_required
def profile(request):
    patient = patient_models.Patient.objects.get(user=request.user)

    if request.method == 'POST':
        patient.full_name = request.POST.get('full_name')
        patient.mobile = request.POST.get('mobile')
        patient.address = request.POST.get('address')
        patient.bood_group = request.POST.get('bood_group')

        date_str = request.POST.get('date_of_birth')
        if date_str:
            naive_date = datetime.strptime(date_str, "%Y-%m-%d")
            aware_date = timezone.make_aware(naive_date)
            patient.date_of_birth = aware_date
            print('PATIENT AGE:', aware_date)


        # ✅ Handle image upload (note: POST.get won't work for files)
        if 'image' in request.FILES:
            patient.image = request.FILES['image']

        patient.save()
        messages.success(request, 'Profile Updated Successfully')
        return redirect('patient:profile')

    context = {
        'patient': patient,
    }
    return render(request, 'patient/profile.html', context)