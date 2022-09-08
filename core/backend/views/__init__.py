from .agency import *
from .booking import *
from .category import *
from .seat import *
from .trip import *
from .vehicle import *
from .ticket import *
from .transaction import *
from .users import *
from .wallets import *
from core.utils.util_functions import get_api_wallet_balance


class DashboardView(View):
    template = "backend/index.html"

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        user_agency = request.user.agency
        if request.user.is_staff or request.user.is_superuser:
            total_users = User.objects.count()
            agencies = Agency.objects.all().count()
            vehicles = Vehicle.objects.all().count()
            seats = Seat.objects.all().count()
            trips = Trip.objects.all().count()
            bookings = Booking.objects.all().count()
            tickets = Ticket.objects.all().count()
            transactions = Transaction.objects.all().count()
            wallet_balance = get_api_wallet_balance()
        elif request.user.is_agency_admin:
            total_users = User.objects.filter(agency=user_agency).count()  # noqa
            agencies = Agency.objects.filter(id=user_agency.id).count()
            vehicles = Vehicle.objects.filter(agency=user_agency).count()  # noqa
            seats = Seat.objects.filter(vehicle__agency=user_agency).count()  # noqa
            trips = Trip.objects.filter(vehicle__agency=user_agency).count()  # noqa
            bookings = Booking.objects.filter(trip__vehicle__agency=user_agency).count()  # noqa
            tickets = Ticket.objects.filter(
                transaction__booking__trip__vehicle__agency=user_agency).count()
            transactions = Transaction.objects.filter(
                booking__trip__vehicle__agency=user_agency).count()
            wallet_balance = request.user.agency.wallet.get_wallet_balance()
        categories = VehicleCategory.objects.all().count()

        context = {
            "total_users": total_users,
            "agencies": agencies,
            "vehicles": vehicles,
            "seats": seats,
            "trips": trips,
            "categories": categories,
            "bookings": bookings,
            "tickets": tickets,
            "transactions": transactions,
            "wallet_balance": wallet_balance,
        }
        return render(request, self.template, context)
