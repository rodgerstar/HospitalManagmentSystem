import random

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from main.app_forms import PatientForm, DoctorForm, MedicalRecordForm
from main.models import Patient, Doctor, Appointment


# Create your views here.
def dashboard(request):
    appointments = Appointment.objects.all()  # You can filter this as needed
    context = {
        'appointments': appointments,
    }
    return render(request, 'dashboard.html', context)


def patients(request):
    data = Patient.objects.all().order_by('-id').values()
    return render(request, 'patients.html', {'data': data})


def doctors(request):
    medics = Doctor.objects.all()
    return render(request, 'doctors.html', {"medics": medics})


def patient_detail(request, patient_id):
    # Fetch the patient using the provided ID
    patient = get_object_or_404(Patient, id=patient_id)

    # Fetch all related medical records for the patient
    medical_records = patient.medical_records.all()  # This fetches all medical records related to the patient

    # Render the template and pass the patient and their medical records
    return render(request, 'patient_details.html', {
        'patient': patient,
        'medical_records': medical_records
    })


def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Patient {form.cleaned_data['first_name']} was successfully added!')
            return redirect('patients')
    else:
        form = PatientForm()
    return render(request, 'patient_form.html', {'form': form})


def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    patient.delete()
    messages.error(request, f'Patient {patient.first_name} was successfully deleted!')
    return redirect('patients')

def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor.delete()
    messages.error(request, f'Doctor{doctor.first_name} was successfully deleted!')
    return redirect('doctors')


def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm( request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Doctor {form.cleaned_data['first_name']} was successfully added!')
            return redirect('doctors')
    else:
        form = DoctorForm()
    return render(request, 'doctor_form.html', {'form': form})




def add_medical_record(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.patient = patient
            medical_record.save()
            messages.success(request, f'Medical record  for patient was successfully added!')
            return redirect('patient_detail', patient_id=patient.id)
    else:
        form = MedicalRecordForm()
    return render(request, 'add_medical_record.html', {'form': form, 'patient': patient})


def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'doctors_detail.html', {'doctor': doctor})


import random
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .models import Patient, Doctor, Appointment

def book_appointment(request, patient_id):
    # Fetch the patient by their ID
    patient = get_object_or_404(Patient, id=patient_id)

    # Get a list of all doctors
    doctor = list(Doctor.objects.all())
    if not doctors:
        return HttpResponse("No doctors available for appointment.", status=404)

    # Randomly select a doctor
    doctor = random.choice(doctor)

    # Create an appointment
    appointment = Appointment.objects.create(patient=patient, doctor=doctor)

    # Use the appointment variable in the response
    return render(request, 'appointment_success.html', {
        'appointment': appointment,
    })
