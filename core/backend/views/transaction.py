from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from core.utils.decorators import MustLogin

from backend.models import Transaction


class TransactionListView(View):
    template = "backend/lists/transactions.html"

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        transactions = Transaction.objects.all().order_by('-id')
        context = {'transactions': transactions}
        return render(request, self.template, context)
