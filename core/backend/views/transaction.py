from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin

from core.utils.decorators import MustLogin

from backend.models import Transaction


class TransactionListView(PermissionRequiredMixin, View):
    permission_required = [
        "backend.view_transaction",
    ]
    template = "backend/lists/transactions.html"

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            transactions = Transaction.objects.all().order_by('-created_at')
        elif request.user.is_agency_admin:
            transactions = Transaction.objects.filter(
                booking__trip__vehicle__agency=request.user.agency)
        context = {'transactions': transactions}
        return render(request, self.template, context)
