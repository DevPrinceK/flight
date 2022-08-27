from django.shortcuts import render
from django.views import View

from backend.models import Transaction


class TransactionListView(View):
    template = "backend/lists/transactions.html"

    def get(self, request, *args, **kwargs):
        transactions = Transaction.objects.all().order_by('-id')
        context = {'transactions': transactions}
        return render(request, self.template, context)
