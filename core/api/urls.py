from django.urls import path
from knox import views as knox_views
from . import views

app_name = "api"
urlpatterns = [
    path("", views.OverviewAPI.as_view(), name="overview"),
    path('sign-up/', views.SignUpAPI.as_view(), name="sign_up"),
    path('user-profile/', views.UserProfileAPI.as_view(), name="user_profile"),
]

# TRIPS ENDPOINTS
urlpatterns += [
    path('search-trips/', views.SearchTripsAPI.as_view(), name="search_trips"),  # noqa
    path('book-trip/', views.BookTripAPI.as_view(), name="book_trip"),
    path('user-bookings/', views.UserBookings.as_view(), name="user_bookings"),  # noqa
]


# PAYMENT ENDPOINTS
urlpatterns += [
    path('pay-for-trip/', views.PayForTripAPI.as_view(), name="pay_for_trip"),  # noqa
]


# SEATS ENDPOINTS
urlpatterns += [
    path('get-vehicle-seats/', views.VehicleSeatsAPI.as_view(), name="get_vehicle_seats"),  # noqa
]


# USER TICKETS ENDPOINTS
urlpatterns += [
    path('get-ticket/', views.GetTicketAPI.as_view(), name="get_ticket"),  # noqa
    path('user-tickets/', views.UserTicketsAPI.as_view(), name="user_tickets"),  # noqa
]


# LOCATIONS
urlpatterns += [
    path('locations/', views.AllLocationsAPI.as_view(), name="locations"),
]


# CATEGORIES
urlpatterns += [
    path('categories/', views.AllCategoriesAPI.as_view(), name="categories"),
]


# AGENCY ENDPOINTS
urlpatterns += [
    path('all-agencies/', views.GetAgenciesAPI.as_view(), name="agencies"),
]

# OTHER TRIP ENDPOINTS
urlpatterns += [
    path('all-trips/', views.AllTripsAPI.as_view(), name="all_trips"),
    path('trips-today/', views.TripsTodayAPI.as_view(), name="trips_today"),
]


# KNOX AUTHENTICATION
urlpatterns += [
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),  # noqa
]
