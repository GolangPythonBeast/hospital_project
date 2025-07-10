from django.shortcuts import render, redirect
from base.models import Services, Appointment, Billing
from doctor.models import Doctor
from patient.models import Patient
from django.contrib.auth.decorators import login_required

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
        billing.tax = appointment.service * 5 / 100
        billing.total = billing.sub_total + billing.tax
        billing.status = "Unpaid"
        return redirect('checkout', billing.billing_id)

    context = {
        'service': service,
        'doctor': doctor,
        'patient': patient,
    }
    return render(request, 'book-appointment.html', context)
