"""
URL configuration for hospitalms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from main import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('invoices', views.all_invoices, name='all_invoices'),
    path('doctors', views.doctors, name='doctors'),
    path('patients', views.patients, name='patients'),
    path('add/doctor', views.add_doctor, name='add_doctor'),
    path('add/patient', views.add_patient, name='add_patient'),
    path('patient-details/<int:patient_id>', views.patient_detail, name='patient_detail'),
    path('doctor-details/<int:doctor_id>', views.doctor_detail, name='doctor_detail'),
    path('pay/<int:patient_id>', views.pay_bills, name='pay_bills'),
    path('invoices/create/<int:patient_id>/', views.create_invoice, name='create_invoice'),
    path('book-appointment/<int:patient_id>', views.book_appointment, name='book_appointment'),
    path('handle/payment/transactions', views.callback, name='callback'),
    path('patient/<int:patient_id>/add_record/', views.add_medical_record, name='add_medical_record'),
    path('patient/delete/<int:patient_id>', views.delete_patient, name='delete_patient'),
    path('patient/delete/<int:doctor_id>', views.delete_doctor, name='delete_doctor'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_page, name='logout'),
    path('admin/', admin.site.urls),
]
