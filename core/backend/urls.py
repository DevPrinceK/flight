from django.urls import path
from . import views

app_name = "backend"
urlpatterns = [
    path("", views.DashboardView.as_view(), name="backend"),
]

# VEHICLES
urlpatterns += [
    path("vehicles/", views.VehicleListView.as_view(), name="vehicles"),
]

# TRANSACTIONS
urlpatterns += [
    path("transactions/", views.TransactionListView.as_view(), name="transactions"),
]

# BOOKINGS
urlpatterns += [
    path("bookings/", views.BookingListView.as_view(), name="bookings"),
]

# TICKETS
urlpatterns += [
    path("tickets/", views.TicketListView.as_view(), name="tickets"),
]
