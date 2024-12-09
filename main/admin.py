from django.contrib import admin

from main.models import Patient, Doctor, Appointment, MedicalRecord, Invoice, Department


# Register your models here.
admin.site.site_header = 'MOH ms'
admin.site.site_title = 'MOH Hospital ms'

class PatientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone_number', 'gender', 'address']
    search_fields = ['first_name', 'last_name', 'phone_number', 'gender', 'address']
    list_per_page = 30

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'gender', 'department']
    search_fields = ['first_name', 'last_name', 'email', 'gender', 'department']
    list_per_page = 10

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'date', 'time', 'status']
    search_fields = ['patient', 'date', 'time', 'status']
    list_per_page = 10

class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'diagnosis', 'prescription', 'visit_date']
    search_fields = ['patient', 'diagnosis', 'prescription', 'visit_date']
    list_per_page = 30

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['patient', 'amount', 'description']
    search_fields = ['patient', 'amount', 'description']
    list_per_page = 30

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'qualifications', 'age']


admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(MedicalRecord, MedicalRecordAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Department, DepartmentAdmin)
