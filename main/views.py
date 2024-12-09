from django.shortcuts import render, get_object_or_404

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
    return None


def delete_patient(request):
    return None