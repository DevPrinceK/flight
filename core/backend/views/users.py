from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.utils.html import strip_tags
from django.utils.decorators import method_decorator
from accounts.models import User
from core.utils.decorators import MustLogin


class UserListView(PermissionRequiredMixin, View):
    template = "backend/lists/users.html"
    permission_required = [
        "accounts.view_user",
    ]

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            users = User.objects.all().order_by('-id')
        elif request.user.is_agency_admin:
            users = User.objects.filter(agency=request.user.agency)
        context = {'users': users}
        return render(request, self.template, context)
