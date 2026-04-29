from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),
    path('doctor/<int:doctor_id>/slots/', views.slot_list, name='slot_list'),
    path('book/<int:slot_id>/', views.book_appointment, name='book_appointment'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('edit/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/doctors/', views.manage_doctors, name='manage_doctors'),
    path('dashboard/doctors/add/', views.add_doctor, name='add_doctor'),
    path('dashboard/doctors/edit/<int:doctor_id>/', views.edit_doctor, name='edit_doctor'),
    path('dashboard/doctors/delete/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),

    path('dashboard/slots/', views.manage_slots, name='manage_slots'),
    path('dashboard/slots/add/', views.add_slot, name='add_slot'),
    path('dashboard/slots/edit/<int:slot_id>/', views.edit_slot, name='edit_slot'),
    path('dashboard/slots/delete/<int:slot_id>/', views.delete_slot, name='delete_slot'),

    path('dashboard/appointments/', views.manage_appointments, name='manage_appointments'),
    path('dashboard/appointments/cancel/<int:appointment_id>/', views.admin_cancel_appointment, name='admin_cancel_appointment'),

    path('dashboard/patients/', views.manage_patients, name='manage_patients'),
    path('dashboard/patients/delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]