from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.utils.html import strip_tags

from backend.models import VehicleCategory
from backend.forms import VehicleCategoryForm


class CategoryListView(View):
    template = "backend/lists/categories.html"

    def get(self, request, *args, **kwargs):
        categories = VehicleCategory.objects.all().order_by('-id')
        context = {'categories': categories}
        return render(request, self.template, context)


class CreateUpdateCategory(View):
    template = "backend/create_update_category.html"

    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('category_id')
        category = VehicleCategory.objects.filter(id=category_id).first()
        context = {"category": category}  # noqa
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        category_id = request.POST.get('category_id')

        if category_id:
            # agency exists
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
            # it's a new agency
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


class DeleteCategory(View):
    def get(self, request, *args, **kwargs):
        return redirect('backend:categories')

    def post(self, request, *args, **kwargs):
        category_id = request.POST.get('category_id')
        category = VehicleCategory.objects.filter(id=category_id).first()
        category.delete()
        messages.success(request, 'Vehicle Category Deleted Successfully.')
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
