from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.AccountLoginView.as_view()),
    path("register/", views.AccountRegisterView.as_view()),
]
