from django.shortcuts import render, HttpResponse
from django.views import View


class AccountLoginPage(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Login Page")
