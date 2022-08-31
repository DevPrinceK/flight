from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.utils.html import strip_tags
from django.utils.decorators import method_decorator


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
        agencies = Agency.objects.all().order_by('-id')
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
        agency = Agency.objects.filter(id=agency_id).first()
        context = {"agency": agency}
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        agency_id = request.POST.get('agency_id')

        if agency_id:
            # agency exists
            agency = Agency.objects.filter(id=agency_id).first()
            form = AgencyForm(request.POST, request.FILES, instance=agency)  # noqa
            if form.is_valid():
                agency = form.save(commit=False)
                agency.save()
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
