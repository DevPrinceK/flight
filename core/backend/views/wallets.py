import decimal
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
from core.utils.util_functions import get_api_wallet_balance, get_transaction_status, make_payment


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
            "VOD": "VODA",
        }
        context = {
            "networks": networks,
        }
        return render(request, self.template, context)

    def generate_transaction_id(self):
        return int(round(time.time() * 10000))

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        phone = request.POST.get('source_phone')
        amount = request.POST.get('amount')
        network = request.POST.get('network')
        transaction_id = self.generate_transaction_id()
        can_proceed_with_transaction = False
        if request.user.is_staff or request.user.is_superuser:
            if (get_api_wallet_balance() > 1) and (get_api_wallet_balance() > decimal.Decimal(amount)):
                can_proceed_with_transaction = True
        elif request.user.is_agency_admin:
            agency_balance = request.user.agency.wallet.main_balance
            if (agency_balance > 1) and (agency_balance > decimal.Decimal(amount)):
                can_proceed_with_transaction = True
        if not can_proceed_with_transaction:
            messages.error(request, "Insufficient balance")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        data = {
            'transaction_id': transaction_id,
            'mobile_number': phone,
            'amount': decimal.Decimal(amount),
            'wallet_id': settings.PAYHUB_WALLET_ID,
            'network_code': network,
            'note': 'Cashout',
        }
        # initiate payment
        try:
            make_payment(data)
        except ConnectionError:
            messages.error(
                request, "Connection Error! Ensure you have active internet connection")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        for i in range(5):
            time.sleep(5)
            transaction_status = get_transaction_status(transaction_id)  # noqa
            print(transaction_status)
            if transaction_status['success'] == True:
                print('the transaction was successful')
                break

        transaction = {
            'transaction_id': transaction_id,
            'external_id': "",
            'amount': decimal.Decimal(amount),
            'source_phone': phone,
            'network': network,
            'note': 'Cashout Transaction',
            'status_code': transaction_status['status_code'],
            'status_message': transaction_status['message'],
            'booking': None,
            'transaction_type': "Cashout",
        }
        print("Saving Transaction")
        cashout = Transaction.objects.create(**transaction)
        print('Transaction Saved')
        if cashout.status_code == "000":
            messages.success(request, "Cashout Successful")
            try:
                request.user.agency.wallet.debit_wallet(
                    decimal.Decimal(cashout.amount))
            except Exception as e:
                print(e)
        else:
            messages.success(request, 'Transaction is pending')
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
