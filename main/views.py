import random
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django_daraja.mpesa.core import MpesaClient

from main.app_forms import PatientForm, DoctorForm, MedicalRecordForm, InvoiceForm
from main.models import Patient, Doctor, Appointment, Invoice, Payment


@login_required
# @permission_required('main.view_dashboard', raise_exception=True)
def dashboard(request):
    appointments = Appointment.objects.all()
    return render(request, 'dashboard.html', {'appointments': appointments})


@login_required
# @permission_required('main.view_patient', raise_exception=True)
def patients(request):
    data = Patient.objects.all().order_by('-id')
    return render(request, 'patients.html', {'data': data})


@login_required
# @permission_required('main.view_doctor', raise_exception=True)
def doctors(request):
    medics = Doctor.objects.all()
    return render(request, 'doctors.html', {"medics": medics})


@login_required
# @permission_required('main.view_patient', raise_exception=True)
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    medical_records = patient.medical_records.all()
    return render(request, 'patient_details.html', {'patient': patient, 'medical_records': medical_records})


@login_required
# @permission_required('main.add_patient', raise_exception=True)
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Patient {form.cleaned_data['first_name']} was successfully added!")
            return redirect('patients')
    else:
        form = PatientForm()
    return render(request, 'patient_form.html', {'form': form})


@login_required
# @permission_required('main.delete_patient', raise_exception=True)
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    patient.delete()
    messages.success(request, f"Patient {patient.first_name} was successfully deleted!")
    return redirect('patients')


@login_required
# @permission_required('main.delete_doctor', raise_exception=True)
def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor.delete()
    messages.success(request, f"Doctor {doctor.first_name} was successfully deleted!")
    return redirect('doctors')


@login_required
# @permission_required('main.add_doctor', raise_exception=True)
def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Doctor {form.cleaned_data['first_name']} was successfully added!")
            return redirect('doctors')
    else:
        form = DoctorForm()
    return render(request, 'doctor_form.html', {'form': form})


@login_required
# @permission_required('main.add_medicalrecord', raise_exception=True)
def add_medical_record(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.patient = patient
            medical_record.save()
            messages.success(request, "Medical record  was successfully added!")
            return redirect('patient_detail', patient_id=patient.id)
    else:
        form = MedicalRecordForm()
    return render(request, 'add_medical_record.html', {'form': form, 'patient': patient})


@login_required
# @permission_required('main.view_doctor', raise_exception=True)
def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'doctors_detail.html', {'doctor': doctor})


@login_required
# @permission_required('main.add_appointment', raise_exception=True)
def book_appointment(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    doctors = list(Doctor.objects.all())
    if not doctors:
        return HttpResponse("No doctors available for appointment.", status=404)
    doctor = random.choice(doctors)
    appointment = Appointment.objects.create(patient=patient, doctor=doctor)
    return render(request, 'appointment_success.html', {'appointment': appointment})


@login_required
# @permission_required('main.add_invoice', raise_exception=True)
def create_invoice(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            amount = form.save(commit=False)
            amount.patient = patient
            amount.save()
            messages.success(request, "Invoice created successfully!")
            return redirect('all_invoices')
    else:
        form = InvoiceForm()
    return render(request, 'create_invoice.html', {'form': form, 'patient': patient})

@login_required
# @permission_required('main.add_payment', raise_exception=True)
@login_required
def pay_bills(request, patient_id):
    invoices = Invoice.objects.filter(patient_id=patient_id, status='Unpaid')
    if not invoices.exists():
        messages.error(request, "No unpaid invoices found for this patient.")
        return redirect('patients')

    for invoice in invoices:
        cl = MpesaClient()
        response = cl.stk_push(
            phone_number= invoice.patient.phone_number,
            amount=int(invoice.amount),  # Testing amount
            account_reference=invoice.patient.first_name,
            transaction_desc='Bill Payment',
            callback_url='https://your-callback-url.example.com'
        )

        if response.response_code == '0':
            Payment.objects.create(
                transaction=invoice,
                merchant_request_id=response.merchant_request_id,
                checkout_request_id=response.checkout_request_id,
                amount='1'  # Testing amount
            )
            invoice.status = 'Payment Triggered'
        else:
            invoice.status = 'Payment Failed'
        invoice.save()

    messages.success(request, "Payment triggered for all unpaid invoices.")
    return redirect('all_invoices')

@csrf_exempt
def callback(request):
    try:
        resp = json.loads(request.body)
        data = resp['Body']['stkCallback']
        if data["ResultCode"] == "0":
            merchant_id = data['MerchantRequestId']
            checkout_id = data['CheckoutRequestId']
            code = next(item['value'] for item in data['CallbackMetadata']['Item'] if item['Name'] == 'MpesaReceiptNumber')
            transaction = Payment.objects.get(merchant_request_id=merchant_id, checkout_request_id=checkout_id)
            transaction.code = code
            transaction.save()

            # Update invoice status to "Paid"
            invoice = transaction.transaction
            invoice.status = 'Paid'
            invoice.save()
    except KeyError:
        return HttpResponse("Invalid data received", status=400)
    return HttpResponse("OK")


@login_required
# @permission_required('main.invoice', raise_exception=True)
def all_invoices(request):
    invoices = Invoice.objects.select_related('patient').all()
    return render(request, 'invoice.html', {'invoices': invoices})

# @permission_required('main.view_dashboard', raise_exception=True)
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')


@login_required
def logout_page(request):
    logout(request)
    return redirect('login')
