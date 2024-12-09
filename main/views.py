from django.shortcuts import render

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


def patient_detail(request):
    return render(request, 'patient_form.html')


def add_patient(request):
    return None