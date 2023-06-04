from django.urls import path
from . import views

urlpatterns = [
    path("", views.ExpenseListCreateView.as_view()),
    path("<uuid:expense_id>/", views.RetriveUpdateExpenseView.as_view()),
]
