from django.urls import path
from . import views

urlpatterns = [
    path("", views.ExpenseListCreateView.as_view()),
    # path("register/", views.AccountRegisterView.as_view()),
]
