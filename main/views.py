from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')


def patients(request):
    return render(request, 'patients.html')


def doctors(request):
    return render(request, 'doctors.html')


def patient_detail(request):
    return render(request, 'patient_form.html')


def add_patient(request):
    return None