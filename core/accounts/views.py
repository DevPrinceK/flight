from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, Permission
import datetime


from backend.forms import AgencyForm
from accounts.manager import AccountManager
from .models import User


class RegisterAgencyView(View):
    template = "accounts/register.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {})

    def post(self, request, *args, **kwargs):
        form = AgencyForm(request.POST, request.FILES or None)
        user_email = request.POST.get("user_email")
        user_password = request.POST.get("password")
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        if form.is_valid():
            agency = form.save()
            if agency:
                # agency is created so go ahead and create an admin use for agency
                user = User.objects.create_agency_admin(
                    email=user_email,
                    password=user_password,
                )
                if user:
                    # user is created so go ahead and assign agency to user
                    user.agency = agency
                    user.first_name = first_name
                    user.last_name = last_name
                    # assign group to user
                    group, created = Group.objects.get_or_create(name="Agency")
                    user.groups.add(group)
                    user.save()
                    # login user after a successful registration
                    # user = authenticate(
                    #     email=user_email,
                    #     password=user_password,
                    # )
                    # if user:
                    #     login(request, user)
                    #     messages.success(
                    #         request, f"Hello {user.first_name}, Welcome to EasyGo!")
                    #     return redirect("backend:backend")
                    # else:
                    #     return HTTPResponse("Something went wrong! Contact admins.")
                    messages.info(request, "Request Submitted Successfully")
                    return redirect("accounts:login")
        messages.success(request, "Agency Not Created Contact Admins!")
        return redirect("accounts:login")


class LoginView(View):
    template = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user.last_login = datetime.datetime.now()
            messages.success(request, 'Hi there, {}'.format(user.first_name))
            return redirect('backend:backend')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('accounts:login')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('accounts:login')
