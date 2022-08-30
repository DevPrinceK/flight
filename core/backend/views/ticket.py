from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from core.utils.decorators import MustLogin
from backend.models import Ticket


class TicketListView(View):
    template = "backend/lists/tickets.html"

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        tickets = Ticket.objects.all().order_by('-id')
        context = {'tickets': tickets}
        return render(request, self.template, context)
