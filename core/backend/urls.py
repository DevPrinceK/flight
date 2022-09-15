from django.urls import path
from . import views

app_name = "backend"
urlpatterns = [
    path("", views.DashboardView.as_view(), name="backend"),
]

# VEHICLES
urlpatterns += [
    path("vehicles/", views.VehicleListView.as_view(), name="vehicles"),
    path("create-update-vehicle/", views.CreateUpdateVehicle.as_view(), name="create_update_vehicle"),  # noqa
    path("delete-vehicle/", views.DeleteVehicle.as_view(), name="delete_vehicle"),  # noqa
    path("free-vehicle-seats/",
         views.FreeVehicleSeatView.as_view(), name="free_vehicle_seats"),  # noqa
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

# SEATS
urlpatterns += [
    path("seats/", views.SeatListView.as_view(), name="seats"),
    path("create-update-seat/", views.CreateUpdateSeat.as_view(), name="create_update_seat"),  # noqa
    path("delete-seat/", views.DeleteSeat.as_view(), name="delete_seat"),  # noqa
]

# TRIPS
urlpatterns += [
    path("trips/", views.TripListView.as_view(), name="trips"),
    path("create-update-trip/", views.CreateUpdateTrip.as_view(), name="create_update_trip"),  # noqa
    path("delete-trip/", views.DeleteTrip.as_view(), name="delete_trip"),  # noqa
]

# CATEGORIES
urlpatterns += [
    path("categories/", views.CategoryListView.as_view(), name="categories"),
    path("create-update-category/", views.CreateUpdateCategory.as_view(), name="create_update_category"),  # noqa
    path("delete-category/", views.DeleteCategory.as_view(), name="delete_category"),  # noqa
]

# AGENCIES
urlpatterns += [
    path("agencies/", views.AgencyListView.as_view(), name="agencies"),
    path("create-update-agency/", views.CreateUpdateAgency.as_view(), name="create_update_agency"),  # noqa
    path("delete-agency/", views.DeleteAgency.as_view(), name="delete_agency"),  # noqa
    path('agency-details/', views.ApproveDisapproveAgencyView.as_view(),
         name="approve_disapprove_agency"),
]

# USERS
urlpatterns += [
    path("users/", views.UserListView.as_view(), name="users"),
]


# WALLETS
urlpatterns += [
    path("wallets/", views.WalletListView.as_view(), name="wallets"),
    path("cashout/", views.CashoutView.as_view(), name="cashout"),
]
