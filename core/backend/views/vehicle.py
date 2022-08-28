from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.utils.html import strip_tags

from backend.models import Agency, Vehicle
from backend.models import VehicleCategory
from backend.forms import VehicleForm


class VehicleListView(View):
    template = "backend/lists/vehicles.html"

    def get(self, request, *args, **kwargs):
        vehicles = Vehicle.objects.all().order_by('-id')
        context = {'vehicles': vehicles}
        return render(request, self.template, context)


class CreateUpdateVehicle(View):
    template = "backend/create_update_vehicle.html"

    def get(self, request, *args, **kwargs):
        vehicle_id = request.GET.get('vehicle_id')
        vehicle = Vehicle.objects.filter(id=vehicle_id).first()
        agencies = Agency.objects.all()
        categories = VehicleCategory.objects.all().order_by('-id')
        context = {"vehicle": vehicle, "categories": categories, "agencies": agencies}  # noqa
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        vehicle_id = request.POST.get('vehicle_id')
        agency_id = request.POST.get('agency')
        category_id = request.POST.get('category')
        agency = Agency.objects.filter(id=agency_id).first()
        category = VehicleCategory.objects.filter(id=category_id).first()

        if vehicle_id:
            # agency exists
            vehicle = Vehicle.objects.filter(id=vehicle_id).first()
            form = VehicleForm(request.POST, request.FILES, instance=vehicle)  # noqa
            if form.is_valid():
                vehicle = form.save(commit=False)
                vehicle.agency = agency
                vehicle.category = category
                vehicle.save()
                messages.success(request, 'Vehicle Details Updated Successfully.')  # noqa
                return redirect('backend:vehicles')
            else:
                for field, error in form.errors.items():
                    message = f"{field.title()}: {strip_tags(error)}"
                    break
                messages.warning(request, message)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            # it's a new agency
            form = VehicleForm(request.POST, request.FILES)
            if form.is_valid():
                vehicle = form.save(commit=False)
                vehicle.agency = agency
                vehicle.category = category
                vehicle.save()
                messages.success(request, 'New Vehicle Created Successfully.')  # noqa
                return redirect('backend:vehicles')
            else:
                for field, error in form.errors.items():
                    message = f"{field.title()}: {strip_tags(error)}"
                    break
                messages.warning(request, message)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class DeleteVehicle(View):
    def get(self, request, *args, **kwargs):
        return redirect('backend:vehicles')

    def post(self, request, *args, **kwargs):
        vehicle_id = request.POST.get('vehicle_id')
        vehicle = Vehicle.objects.filter(id=vehicle_id).first()
        vehicle.delete()
        messages.success(request, 'Vehicle Deleted Successfully.')
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
