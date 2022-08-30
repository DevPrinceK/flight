from .agency import *
from .booking import *
from .category import *
from .seat import *
from .trip import *
from .vehicle import *
from .ticket import *
from .transaction import *


class DashboardView(View):
    template = "backend/index.html"

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template, context)
