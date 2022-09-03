import time
from core import settings
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.utils.html import strip_tags
from django.utils.decorators import method_decorator
from api.serializers import PaymentSerializer
from core.utils.decorators import MustLogin
from backend.models import Transaction, Wallet
from core.utils.util_functions import get_transaction_status, make_payment


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


class CashoutView(PermissionRequiredMixin, View):
    template = "backend/create_update_cashout.html"

    permission_required = [
        "backend.cashout_from_wallet",
    ]

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        networks = {
            "MTN": "MTN",
            "VODA": "VODA",
        }
        context = {
            "networks": networks,
        }
        return render(request, self.template, context)

    def generate_transaction_id(self):
        return int(round(time.time() * 10000))

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)
        # get the particular booking
        if serializer.is_valid():
            serializer.save()
            transaction_id = self.generate_transaction_id()
            data = {
                'transaction_id': transaction_id,
                'mobile_number': serializer['source_phone'].value,
                'amount': serializer['amount'].value,
                'wallet_id': settings.PAYHUB_WALLET_ID,
                'network_code': serializer['network'].value,
                'note': 'Cashout',
            }
            # initiate payment
            make_payment(data)

            for i in range(4):
                time.sleep(5)
                transaction_status = get_transaction_status(transaction_id)  # noqa
                print(transaction_status)
                if transaction_status['success'] == True:
                    print('the transaction was successful')
                    break

            transaction = {
                'transaction_id': transaction_id,
                'external_id': "",
                'amount': serializer['amount'].value,
                'source_phone': serializer['source_phone'].value,
                'network': serializer['network'].value,
                'note': 'Payment for booking service',
                'status_code': transaction_status['status_code'],
                'status_message': transaction_status['message'],
                'booking': None,
            }
            print("Saving Transaction")
            Transaction.objects.create(**transaction)
            print('Transaction Saved')
            messages.success(request, 'Cashout was successful')
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        # if transaction data is not valid
        messages.error(request, 'Cashout could not be processed')
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
