from django import forms
from main.models import Patient, Doctor, MedicalRecord


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'dob',
            'address',
            'gender',
            'visit_date',
            'weight',
            'diagnosis'
        ]
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone_number': 'Phone Number',
            'dob': 'Date of Birth',
            'address': 'Address',
            'gender': 'Gender',
            'visit_date': 'Visit Date',
            'weight': 'Weight',
            'diagnosis': 'Diagnosis',
        }
        help_texts = {
            'phone_number': 'Enter a valid phone number, e.g., 0701234567.',
            'diagnosis': 'Brief diagnosis or symptoms for the visit.',
        }


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            'first_name',
            'last_name',
            'email',
            'department',
            'gender',
            'dob',
            'phone_number',
            'med_reg_num'
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'doctor@example.com'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'department': 'Department',
            'gender': 'Gender',
            'phone_number': 'Phone Number',
            'med_reg_num': 'Medical Registration Number',
        }
        help_texts = {
            'email': 'Enter a valid email address.',
            'med_reg_num': 'Unique registration number issued to the doctor.',
        }

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['diagnosis', 'prescription','notes', 'doctor']

