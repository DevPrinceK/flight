from django.shortcuts import render
from django.views import View

from backend.models import Ticket


class TicketListView(View):
    template = "backend/lists/tickets.html"

    def get(self, request, *args, **kwargs):
        tickets = Ticket.objects.all().order_by('-id')
        context = {'tickets': tickets}
        return render(request, self.template, context)
