from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.utils.html import strip_tags
from django.utils.decorators import method_decorator
from accounts.models import User


from backend.models import Agency
from backend.forms import AgencyForm
from core.utils.decorators import MustLogin


class AgencyListView(PermissionRequiredMixin, View):
    permission_required = [
        "backend.view_agency",
    ]
    template = "backend/lists/agencies.html"

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            agencies = Agency.objects.all().order_by('-id')
        elif request.user.is_agency_admin:
            agencies = Agency.objects.filter(id=request.user.agency.id)
        context = {'agencies': agencies}
        return render(request, self.template, context)


class CreateUpdateAgency(PermissionRequiredMixin, View):
    permission_required = [
        "backend.change_agency",
        "backend.add_agency",
    ]
    template = "backend/create_update_agency.html"

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        agency_id = request.GET.get('agency_id')
        if request.user.is_staff or request.user.is_superuser:
            agency = Agency.objects.filter(id=agency_id).first()
            admins = User.objects.filter(is_staff=False, is_superuser=False)
        elif request.user.is_agency_admin:
            agency = Agency.objects.filter(id=request.user.agency.id).first()
        context = {"agency": agency, "admins": admins}
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        agency_id = request.POST.get('agency_id')
        agency_admin_id = request.POST.get('agency_admin')

        if agency_admin_id:
            agency_admin = User.objects.filter(id=int(agency_admin_id)).first()  # noqa
            agency_admin.is_agency_admin = True
            agency_admin.save()
        else:
            agency_admin = None

        if agency_id:
            # agency exists
            if request.user.is_staff or request.user.is_superuser:
                agency = Agency.objects.filter(id=agency_id).first()
            elif request.user.is_agency_admin:
                agency = Agency.objects.filter(
                    id=request.user.agency.id).first()
            form = AgencyForm(request.POST, request.FILES, instance=agency)  # noqa
            if form.is_valid():
                agency = form.save(commit=False)
                agency.save()
                if agency_admin:
                    agency_admin.agency = agency
                    agency_admin.save()
                messages.success(request, 'Agency Details Updated Successfully.')  # noqa
                return redirect('backend:agencies')
            else:
                for field, error in form.errors.items():
                    message = f"{field.title()}: {strip_tags(error)}"
                    break
                messages.warning(request, message)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            # it's a new agency
            form = AgencyForm(request.POST, request.FILES)
            if form.is_valid():
                agency = form.save(commit=False)
                agency.save()
                if agency_admin:
                    agency_admin.agency = agency
                    agency_admin.save()
                messages.success(request, 'New Agency Created Successfully.')  # noqa
                return redirect('backend:agencies')
            else:
                for field, error in form.errors.items():
                    message = f"{field.title()}: {strip_tags(error)}"
                    break
                messages.warning(request, message)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class DeleteAgency(PermissionRequiredMixin, View):
    permission_required = [
        "backend.delete_agency",
    ]

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        return redirect('backend:agencies')

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        agency_id = request.POST.get('agency_id')
        if request.user.is_staff or request.user.is_superuser:
            agency = Agency.objects.filter(id=agency_id).first()
            agency.delete()
            messages.success(request, 'Agency Deleted Successfully.')
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, "Permission Denied!")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class ApproveDisapproveAgencyView(View):
    permission_required = [
        "backend.can_approve_disapprove_agency",
    ]

    template = "backend/details/agency_details.html"

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        agency_id = request.GET.get('agency_id')
        agency = Agency.objects.filter(id=int(agency_id)).first()
        context = {
            'agency': agency,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        agency_id = request.POST.get('agency_id')
        status_id = request.POST.get('status_id')
        status = True if status_id == 'on' else False
        agency = Agency.objects.filter(id=int(agency_id)).first()
        try:
            agency.is_approved = status
            agency.save()
        except Exception as e:
            print(e)
            messages.error(request, "Agency Status Couldn't Be Changed!")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        if status:
            messages.success(request, "Travel Agency Approved!")
        else:
            messages.success(request, "Agency's approval status revoked!")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
