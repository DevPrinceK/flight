from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.utils.html import strip_tags
from django.utils.decorators import method_decorator
from core.utils.decorators import MustLogin
from backend.models import Wallet


class WalletListView(PermissionRequiredMixin, View):
    template = "backend/lists/wallets.html"
    permission_required = [
        "backend.view_wallet",
    ]

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            wallets = Wallet.objects.all().order_by('-id')
        elif request.user.is_agency_admin:
            wallets = {request.user.agency.wallet}
        context = {'wallets': wallets}
        return render(request, self.template, context)
