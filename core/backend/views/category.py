from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.utils.html import strip_tags

from backend.models import VehicleCategory
from backend.forms import VehicleCategoryForm
from core.utils.decorators import MustLogin


class CategoryListView(PermissionRequiredMixin, View):
    permission_required = [
        "backend.view_vehiclecategory",
    ]
    template = "backend/lists/categories.html"

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        categories = VehicleCategory.objects.all().order_by('-id')
        context = {'categories': categories}
        return render(request, self.template, context)


class CreateUpdateCategory(PermissionRequiredMixin, View):
    permission_required = [
        "backend.add_vehiclecategory",
        "backend.change_vehiclecategory",
    ]
    template = "backend/create_update_category.html"

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('category_id')
        category = VehicleCategory.objects.filter(id=category_id).first()
        context = {"category": category}  # noqa
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        category_id = request.POST.get('category_id')

        if category_id:
            # category exists
            category = VehicleCategory.objects.filter(id=category_id).first()
            form = VehicleCategoryForm(request.POST, request.FILES, instance=category)  # noqa
            if form.is_valid():
                category = form.save(commit=False)
                category.save()
                messages.success(request, 'Vehicle Category Details Updated Successfully.')  # noqa
                return redirect('backend:categories')
            else:
                for field, error in form.errors.items():
                    message = f"{field.title()}: {strip_tags(error)}"
                    break
                messages.warning(request, message)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            # it's a new category
            form = VehicleCategoryForm(request.POST, request.FILES)
            if form.is_valid():
                category = form.save(commit=False)
                category.save()
                messages.success(request, 'New Vehicle Category Created Successfully.')  # noqa
                return redirect('backend:categories')
            else:
                for field, error in form.errors.items():
                    message = f"{field.title()}: {strip_tags(error)}"
                    break
                messages.warning(request, message)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class DeleteCategory(PermissionRequiredMixin, View):
    permission_required = [
        "backend.delete_vehiclecategory",
    ]

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        return redirect('backend:categories')

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        category_id = request.POST.get('category_id')
        category = VehicleCategory.objects.filter(id=category_id).first()
        category.delete()
        messages.success(request, 'Vehicle Category Deleted Successfully.')
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
