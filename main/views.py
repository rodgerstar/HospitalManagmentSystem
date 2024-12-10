from django.shortcuts import render, get_object_or_404

from main.app_forms import PatientForm, DoctorForm
from main.models import Patient, Doctor


# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')


def patients(request):
    data = Patient.objects.all()
    return render(request, 'patients.html', {'data': data})


def doctors(request):
    medics = Doctor.objects.all()
    return render(request, 'doctors.html', {"medics": medics})


def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'patient_details.html', {"patient":patient})


def add_patient(request):
    form = PatientForm()
    return render(request, 'patient_form.html', {'form': form})


def delete_patient(request, patient_id):
    return None


def add_doctor(request):
    form = DoctorForm()
    return render(request, 'doctor_form.html', {'form': form})


def delete_doctor(request, doctor_id):
    return None