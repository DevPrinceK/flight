from django.urls import path
from . import views

app_name = "api"
urlpatterns = [
    path("", views.HomeAPIView.as_view(), name="home"),
    path('sign-up/', views.SignUpAPI.as_view(), name="sign_up"),
    path('all-trips/', views.AllTripsAPI.as_view(), name="all_trips"),
    path('trips-today/', views.TripsTodayAPI.as_view(), name="trips_today"),
    path('custom-trips/', views.CustomTripsAPI.as_view(), name="custom_trips"),  # noqa
    path('book-trip/', views.BookTripAPI.as_view(), name="book_trip"),
]
