from django.shortcuts import render
from django.views import View
from backend.models import VehicleCategory


class CategoryListView(View):
    template = "backend/lists/categories.html"

    def get(self, request, *args, **kwargs):
        categories = VehicleCategory.objects.all().order_by('-id')
        context = {'categories': categories}
        return render(request, self.template, context)