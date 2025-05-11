from datetime import date, timedelta

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from .forms import ReservationForm, ConferenceRoomForm
from .models import Reservation, ConferenceRoom
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

def redirect_to_login(request):
    return redirect('/accounts/login/')


@login_required
def redirect_after_login(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    else:
        return redirect('make_reservation')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('make_reservation')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            messages.success(request,
                             f"Reservation confirmed for {reservation.room.name} on {reservation.date} at {reservation.start_time}.")
            return redirect('my_reservations')
    else:
        form = ReservationForm()
    return render(request, 'reservations/make_reservation.html', {'form': form})

@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)

    # Check for upcoming reservation within next 1 day
    tomorrow = date.today() + timedelta(days=1)
    upcoming = reservations.filter(date__lte=tomorrow, date__gte=date.today()).first()

    if upcoming:
        messages.info(request,
                      f"Reminder: You have a reservation for {upcoming.room.name} on {upcoming.date} at {upcoming.start_time}.")

    return render(request, 'reservations/my_reservations.html', {'reservations': reservations})


@login_required
def edit_reservation(request, id):
    reservation = Reservation.objects.get(id=id, user=request.user)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('my_reservations')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'reservations/edit_reservation.html', {'form': form})

@login_required
def delete_reservation(request, id):
    reservation = Reservation.objects.get(id=id, user=request.user)
    reservation.delete()
    return redirect('my_reservations')

def is_admin(user):
    return user.is_staff  # You can use is_superuser if needed

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'reservations/admin_dashboard.html')

@login_required
@user_passes_test(is_admin)
def admin_manage_rooms(request):
    return render(request, 'reservations/admin_rooms.html')

@login_required
@user_passes_test(is_admin)
def admin_manage_reservations(request):
    return render(request, 'reservations/admin_reservations.html')

@login_required
@user_passes_test(is_admin)
def admin_manage_users(request):
    return render(request, 'reservations/admin_users.html')

@login_required
@user_passes_test(is_admin)
def admin_manage_rooms(request):
    rooms = ConferenceRoom.objects.all()
    return render(request, 'reservations/admin_rooms.html', {'rooms': rooms})

@login_required
@user_passes_test(is_admin)
def admin_add_room(request):
    if request.method == 'POST':
        form = ConferenceRoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_manage_rooms')
    else:
        form = ConferenceRoomForm()
    return render(request, 'reservations/admin_add_edit_room.html', {'form': form, 'action': 'Add'})

@login_required
@user_passes_test(is_admin)
def admin_edit_room(request, id):
    room = ConferenceRoom.objects.get(id=id)
    if request.method == 'POST':
        form = ConferenceRoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('admin_manage_rooms')
    else:
        form = ConferenceRoomForm(instance=room)
    return render(request, 'reservations/admin_add_edit_room.html', {'form': form, 'action': 'Edit'})

@login_required
@user_passes_test(is_admin)
def admin_delete_room(request, id):
    room = ConferenceRoom.objects.get(id=id)
    room.delete()
    return redirect('admin_manage_rooms')

@login_required
@user_passes_test(is_admin)
def admin_manage_reservations(request):
    reservations = Reservation.objects.select_related('user', 'room').all().order_by('-date', 'start_time')
    return render(request, 'reservations/admin_reservations.html', {'reservations': reservations})

@login_required
@user_passes_test(is_admin)
def admin_delete_reservation(request, id):
    reservation = Reservation.objects.get(id=id)
    reservation.delete()
    return redirect('admin_manage_reservations')

from django.contrib.auth.models import User
from django.contrib import messages

@login_required
@user_passes_test(is_admin)
def admin_manage_users(request):
    users = User.objects.all().order_by('username')
    return render(request, 'reservations/admin_users.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def admin_delete_user(request, id):
    if request.user.id == id:
        messages.error(request, "You can't delete yourself.")
        return redirect('admin_manage_users')
    User.objects.get(id=id).delete()
    messages.success(request, "User deleted successfully.")
    return redirect('admin_manage_users')

@login_required
@user_passes_test(is_admin)
def admin_promote_user(request, id):
    user = User.objects.get(id=id)
    user.is_staff = True
    user.save()
    messages.success(request, f"{user.username} has been promoted to admin.")
    return redirect('admin_manage_users')
