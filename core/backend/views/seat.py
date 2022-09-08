from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.utils.html import strip_tags
from django.utils.decorators import method_decorator

from backend.forms import Seat
from backend.models import Agency, Vehicle
from backend.forms import SeatForm
from core.utils.decorators import MustLogin


class SeatListView(PermissionRequiredMixin, View):
    permission_required = [
        "backend.view_seat",
    ]
    template = "backend/lists/seats.html"

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            seats = Seat.objects.all().order_by('-id')
        elif request.user.is_agency_admin:
            seats = Seat.objects.filter(vehicle__agency=request.user.agency)
        context = {'seats': seats}
        return render(request, self.template, context)


class CreateUpdateSeat(PermissionRequiredMixin, View):
    permission_required = [
        "backend.add_seat",
        "backend.change_seat",
    ]

    template = "backend/create_update_seat.html"

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        seat_id = request.GET.get('seat_id')
        vehicle_id = request.GET.get('vehicle_id')
        if request.user.is_staff or request.user.is_superuser:
            seat = Seat.objects.filter(id=seat_id).first()
            vehicle = Vehicle.objects.filter(id=vehicle_id).first()  # noqa
            vehicles = Vehicle.objects.all()
        elif request.user.is_agency_admin:
            seat = Seat.objects.filter(id=seat_id, vehicle__agency=request.user.agency).first()  # noqa
            vehicle = Vehicle.objects.filter(id=vehicle_id, agency=request.user.agency).first()  # noqa
            vehicles = Vehicle.objects.filter(agency=request.user.agency)
        context = {
            "seat": seat,
            "vehicle": vehicle,
            "vehicles": vehicles,
        }  # noqa
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        seat_id = request.POST.get('seat_id')
        vehicle_id = request.POST.get('vehicle_id')
        if request.user.is_staff or request.user.is_superuser:
            vehicle = Vehicle.objects.filter(id=vehicle_id).first()
        elif request.user.is_agency_admin:
            vehicle = Vehicle.objects.filter(id=vehicle_id, agency=request.user.agency).first()  # noqa

        if seat_id:
            # seat exists - update seat
            if request.user.is_staff or request.user.is_superuser:
                seat = Seat.objects.filter(id=seat_id).first()
            elif request.user.is_agency_admin:
                seat = Seat.objects.filter(id=seat_id, vehicle__agency=request.user.agency).first()  # noqa
            form = SeatForm(request.POST, request.FILES, instance=seat)  # noqa
            if form.is_valid():
                new_seat = form.save(commit=False)
                new_seat.vehicle = vehicle
                new_seat.save()
                messages.success(request, 'Seat Detail Updated Successfully.')  # noqa
                return redirect('backend:seats')
            else:
                for field, error in form.errors.items():
                    message = f"{field.title()}: {strip_tags(error)}"
                    break
                messages.warning(request, message)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            # it's a new seat - create seat
            form = SeatForm(request.POST, request.FILES)
            if form.is_valid():
                seat = form.save(commit=False)
                seat.vehicle = vehicle
                seat.save()
                messages.success(request, 'New Seat Created Successfully.')  # noqa
                return redirect('backend:seats')
            else:
                for field, error in form.errors.items():
                    message = f"{field.title()}: {strip_tags(error)}"
                    break
                messages.warning(request, message)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class DeleteSeat(PermissionRequiredMixin, View):
    permission_required = [
        "backend.delete_seat",
    ]

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        return redirect('backend:seats')

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        seat_id = request.POST.get('seat_id')
        if request.user.is_staff or request.user.is_superuser:
            seat = Seat.objects.filter(id=seat_id).first()
        elif request.user.is_agency_admin:
            seat = Seat.objects.filter(
                id=seat_id, vehicle__agency=request.user.agency).first()
        seat.delete()
        messages.success(request, 'Vehicle Seat Deleted Successfully.')
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
