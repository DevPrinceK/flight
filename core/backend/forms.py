from django import forms

from .models import Agency
from .models import Vehicle
from .models import Seat
from .models import VehicleCategory
from .models import Trip


class AgencyForm(forms.ModelForm):
    class Meta:
        model = Agency
        fields = ['name', 'address', 'phone', 'email', 'website', 'contact_person_ID', 'business_certificate']  # noqa


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['name', 'vin']


class SeatForm(forms.ModelForm):
    class Meta:
        model = Seat
        fields = ['seat_num']


class VehicleCategoryForm(forms.ModelForm):
    class Meta:
        model = VehicleCategory
        fields = ['name']


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['source', 'destination', 'price', 'date', 'time']
