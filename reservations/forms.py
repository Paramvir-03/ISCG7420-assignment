from django import forms
from .models import Reservation
from .models import ConferenceRoom

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['room', 'date', 'start_time', 'end_time']

class ConferenceRoomForm(forms.ModelForm):
    class Meta:
        model = ConferenceRoom
        fields = ['name', 'location', 'capacity']
