from django.shortcuts import render, get_object_or_404, redirect

from main.app_forms import PatientForm, DoctorForm, MedicalRecordForm
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
    form = PatientForm()
    return render(request, 'patient_form.html', {'form': form})


def delete_patient(request, patient_id):
    return None


def add_doctor(request):
    form = DoctorForm()
    return render(request, 'doctor_form.html', {'form': form})


def delete_doctor(request, doctor_id):
    return None


def add_medical_record(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.patient = patient
            medical_record.save()
            return redirect('patient_detail', patient_id=patient.id)
    else:
        form = MedicalRecordForm()
    return render(request, 'add_medical_record.html', {'form': form, 'patient': patient})


def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'doctors_detail.html', {'doctor': doctor})