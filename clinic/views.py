from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from .models import Doctor, AppointmentSlot, Appointment
from .forms import RegisterForm

def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'clinic/doctor_list.html', {'doctors': doctors})

def slot_list(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    slots = AppointmentSlot.objects.filter(doctor=doctor, is_booked=False).order_by('date', 'time')
    return render(request, 'clinic/slot_list.html', {'doctor': doctor, 'slots': slots})

@login_required
def book_appointment(request, slot_id):
    slot = get_object_or_404(AppointmentSlot, id=slot_id, is_booked=False)
    Appointment.objects.create(
        patient=request.user,
        slot=slot
    )
    slot.is_booked = True
    slot.save()
    return redirect('my_appointments')

@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user).select_related('slot', 'slot__doctor')
    return render(request, 'clinic/my_appointments.html', {'appointments': appointments})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'clinic/register.html', {'form': form})

@login_required
def book_appointment(request, slot_id):
    slot = get_object_or_404(AppointmentSlot, id=slot_id, is_booked=False)
    Appointment.objects.create(
        patient=request.user,
        slot=slot
    )
    slot.is_booked = True
    slot.save()
    return redirect('my_appointments')

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient=request.user
    )
    slot = appointment.slot
    slot.is_booked = False
    slot.save()
    appointment.delete()
    return redirect('my_appointments')

@login_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient=request.user
    )
    available_slots = AppointmentSlot.objects.filter(is_booked=False).order_by('date', 'time')
    if request.method == 'POST':
        new_slot_id = request.POST.get('slot')
        new_slot = get_object_or_404(AppointmentSlot, id=new_slot_id, is_booked=False)
        old_slot = appointment.slot
        old_slot.is_booked = False
        old_slot.save()
        appointment.slot = new_slot
        appointment.save()
        new_slot.is_booked = True
        new_slot.save()
        return redirect('my_appointments')
    return render(request, 'clinic/edit_appointment.html', {
        'appointment': appointment,
        'available_slots': available_slots
    })

def login_view(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('doctor_list')
        else:
            message = 'Invalid username or password'
    return render(request, 'clinic/login.html', {'message': message})

def logout_view(request):
    logout(request)
    return redirect('login')

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin, login_url='login')
def dashboard(request):
    doctors_count = Doctor.objects.count()
    slots_count = AppointmentSlot.objects.count()
    appointments_count = Appointment.objects.count()
    patients_count = User.objects.filter(is_staff=False).count()
    return render(request, 'clinic/dashboard.html', {
        'doctors_count': doctors_count,
        'slots_count': slots_count,
        'appointments_count': appointments_count,
        'patients_count': patients_count,
    })

@user_passes_test(is_admin, login_url='login')
def manage_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'clinic/manage_doctors.html', {'doctors': doctors})

@user_passes_test(is_admin, login_url='login')
def add_doctor(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        specialty = request.POST.get('specialty')
        Doctor.objects.create(name=name, specialty=specialty)
        return redirect('manage_doctors')
    return render(request, 'clinic/add_doctor.html')

@user_passes_test(is_admin, login_url='login')
def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        doctor.name = request.POST.get('name')
        doctor.specialty = request.POST.get('specialty')
        doctor.save()
        return redirect('manage_doctors')
    return render(request, 'clinic/edit_doctor.html', {'doctor': doctor})


@user_passes_test(is_admin, login_url='login')
def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor.delete()
    return redirect('manage_doctors')

@user_passes_test(is_admin, login_url='login')
def manage_slots(request):
    slots = AppointmentSlot.objects.select_related('doctor').all().order_by('date', 'time')
    return render(request, 'clinic/manage_slots.html', {'slots': slots})

@user_passes_test(is_admin, login_url='login')
def add_slot(request):
    doctors = Doctor.objects.all()
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        time = request.POST.get('time')
        doctor = get_object_or_404(Doctor, id=doctor_id)
        AppointmentSlot.objects.create(
            doctor=doctor,
            date=date,
            time=time
        )
        return redirect('manage_slots')
    return render(request, 'clinic/add_slot.html', {'doctors': doctors})

@user_passes_test(is_admin, login_url='login')
def edit_slot(request, slot_id):
    slot = get_object_or_404(AppointmentSlot, id=slot_id)
    doctors = Doctor.objects.all()
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        slot.doctor = get_object_or_404(Doctor, id=doctor_id)
        slot.date = request.POST.get('date')
        slot.time = request.POST.get('time')
        slot.is_booked = request.POST.get('is_booked') == 'on'
        slot.save()
        return redirect('manage_slots')
    return render(request, 'clinic/edit_slot.html', {
        'slot': slot,
        'doctors': doctors
    })

@user_passes_test(is_admin, login_url='login')
def delete_slot(request, slot_id):
    slot = get_object_or_404(AppointmentSlot, id=slot_id)
    slot.delete()
    return redirect('manage_slots')

@user_passes_test(is_admin, login_url='login')
def manage_appointments(request):
    appointments = Appointment.objects.select_related(
        'patient',
        'slot',
        'slot__doctor'
    ).all().order_by('slot__date', 'slot__time')
    return render(request, 'clinic/manage_appointments.html', {
        'appointments': appointments
    })

@user_passes_test(is_admin, login_url='login')
def admin_cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    slot = appointment.slot
    slot.is_booked = False
    slot.save()
    appointment.delete()
    return redirect('manage_appointments')

@user_passes_test(is_admin, login_url='login')
def manage_patients(request):
    patients = User.objects.filter(is_staff=False).order_by('username')
    return render(request, 'clinic/manage_patients.html', {
        'patients': patients
    })

@user_passes_test(is_admin, login_url='login')
def delete_patient(request, patient_id):
    patient = get_object_or_404(User, id=patient_id, is_staff=False)
    patient.delete()
    return redirect('manage_patients')