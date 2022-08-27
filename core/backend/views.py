from django.shortcuts import render, HttpResponse
from django.views import View


class DashboardView(View):
    template = "backend/index.html"

    def get(self, request, *args, **kwargs):
        context = {}
        # return render(request, self.template, context)
        return render(request, self.template, context)
