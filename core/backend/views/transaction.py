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
        transactions = Transaction.objects.all().order_by('-id')
        context = {'transactions': transactions}
        return render(request, self.template, context)
