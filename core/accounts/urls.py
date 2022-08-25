from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("login/", views.AccountLoginPage.as_view(), name="login"),
]
