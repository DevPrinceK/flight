from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from core.utils.decorators import MustLogin
from backend.models import Ticket


class TicketListView(PermissionRequiredMixin, View):
    permission_required = [
        "backend.view_ticket"
    ]

    template = "backend/lists/tickets.html"

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            tickets = Ticket.objects.all().order_by('-id')
        elif request.user.is_agency_admin:
            tickets = Ticket.objects.filter(
                transaction__booking__trip__vehicle__agency=request.user.agency)
        context = {'tickets': tickets}
        return render(request, self.template, context)
