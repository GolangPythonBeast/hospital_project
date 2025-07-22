from django.shortcuts import render, redirect
from doctor import  models as doctor_models
from base import models as base_models
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.utils import timezone


# Create your views here.
@login_required
def dashboard(request):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(doctor=doctor)
    notifications = doctor_models.Doctor_notification.objects.filter(doctor=doctor)
    context = {
        'appointments': appointments,
        'notifications': notifications,
    }
    return render(request, 'doctor/dashboard.html', context)

@login_required
def appointments(request):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(doctor=doctor)
    context = {
        'appointments': appointments,
    }
    return render(request, 'doctor/appointments.html', context)


@login_required
def appointment_detail(request, appointment_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    medical_records = base_models.MedicalRecord.objects.filter(appointment=appointment)
    lab_tests = base_models.Labtest.objects.filter(appointment=appointment)
    prescriptions = base_models.Prescription.objects.filter(appointment=appointment)

    context = {
        'appointment': appointment,
        'medical_records': medical_records,
        'lab_tests': lab_tests,
        'prescriptions': prescriptions,
    }
    return render(request, 'doctor/appointment_detail.html', context)



@login_required
def cancel_appointment(request, appointment_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    appointment.status = 'Cancelled'
    appointment.save()
    
    messages.success(request, "Appointment cancelled successfully")
    return redirect('doctor:appointment_detail', appointment.appointment_id)


@login_required
def activate_appointment(request, appointment_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    appointment.status = 'Scheduled'
    appointment.save()
    
    messages.success(request, "Appointment Resheduled successfully")
    return redirect('doctor:appointment_detail', appointment.appointment_id)

@login_required
def complete_appointment(request, appointment_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    appointment.status = 'Completed'
    appointment.save()
    
    messages.success(request, "Appointment Completed successfully")
    return redirect('doctor:appointment_detail', appointment.appointment_id)


@login_required
def add_medical_report(request, appointment_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    
    if request.method == 'POST':
        diagnosis = request.POST.get('diagnosis')
        treatment = request.POST.get('treatment')
        base_models.MedicalRecord.objects.create(
            appointment=appointment,
            diagnosis=diagnosis,
            treatment=treatment
        )
        
    messages.success(request, "Mediacl Report Added Successfully")
    return redirect('doctor:appointment_detail', appointment.appointment_id)
        

@login_required
def edit_medical_report(request, appointment_id, medical_report_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    medical_records = base_models.MedicalRecord.objects.get(id=medical_report_id, appointment=appointment)
    
    if request.method == 'POST':
        medical_records.diagnosis = request.POST.get('diagnosis')
        medical_records.treatment = request.POST.get('treatment')
        medical_records.save()
        
    messages.success(request, "Medical Report updated successfully")
    return redirect('doctor:appointment_detail', appointment.appointment_id)
    
    
@login_required
def add_lab_test(request, appointment_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    
    if request.method == 'POST':
        test_name = request.POST.get('test_name')
        description = request.POST.get('description')
        result = request.POST.get('result')
        
        base_models.Labtest.objects.create(appointment=appointment, test_name=test_name, description=description, result=result)
        
    messages.success(request, "Lab Result Added Successfully")
    return redirect('doctor:appointment_detail', appointment.appointment_id)
    
    
@login_required
def edit_lab_test(request, appointment_id, lab_test_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    
    lab_test = base_models.Labtest.objects.get(id=lab_test_id, appointment=appointment)
    
    if request.method == 'POST':
        lab_test.test_name = request.POST.get('test_name')
        lab_test.description = request.POST.get('description')
        lab_test.result = request.POST.get('result')
        
        lab_test.save()
        
    messages.success(request, "Lab Result Updated Successfully")
    return redirect('doctor:appointment_detail', appointment.appointment_id)


@login_required
def set_medication(request, appointment_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    
    if request.method == 'POST':
        medication = request.POST.get('medications')
        base_models.Prescription.objects.create(
            appointment=appointment,
            medication=medication
        )
    messages.success(request, 'Prescription Added Successfully')
    return redirect('doctor:appointment_detail', appointment.appointment_id)

@login_required
def edit_medication(request, appointment_id, medication_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    
    prescription = base_models.Prescription.objects.get(id=medication_id)
    if request.method == 'POST':
        prescription.medication = request.POST.get('medications')
        prescription.save()
        
    messages.success(request, 'Prescription Edited Successfully')
    return redirect('doctor:appointment_detail', appointment.appointment_id)


@login_required
def payments(request):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    payments = base_models.Billing.objects.filter(appointment__doctor=doctor, status='Paid') # filter is used to get more values of payments in a list
    
    context = {
        'payments': payments,
    }
    return render(request, 'doctor/payments.html', context)
    
    
@login_required
def notification(request):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    notifications = doctor_models.Doctor_notification.objects.filter(doctor=doctor, seen=False)
    
    context = {
        'notifications': notifications
    }
    return render(request, 'doctor/notifications.html', context)

@login_required
def make_notification(request, id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    notification = doctor_models.Doctor_notification.objects.get(doctor=doctor, id=id)
    notification.seen = True
    notification.save()
    
    messages.success(request, 'Notication Seen Successfully')
    return redirect('doctor:notification')

@login_required
def profile(request):
    doctor = doctor_models.Doctor.objects.get(user=request.user)

    if request.method == 'POST':
        doctor.full_name = request.POST.get('full_name')
        doctor.mobile = request.POST.get('mobile')
        doctor.country = request.POST.get('country')
        doctor.specialization = request.POST.get('specialization')
        doctor.qualification = request.POST.get('qualifications')
        doctor.years_of_experience = request.POST.get('years_of_experience')
        doctor.bio = request.POST.get('bio')

        date_str = request.POST.get('next_available_appointment_date')
        if date_str:
            naive_date = datetime.strptime(date_str, "%Y-%m-%d")
            aware_date = timezone.make_aware(naive_date)
            doctor.next_available_appointment_date = aware_date


        # ✅ Handle image upload (note: POST.get won't work for files)
        if 'image' in request.FILES:
            doctor.image = request.FILES['image']

        doctor.save()
        messages.success(request, 'Profile Updated Successfully')
        return redirect('doctor:profile')

    context = {
        'doctor': doctor,
    }
    return render(request, 'doctor/profile.html', context)