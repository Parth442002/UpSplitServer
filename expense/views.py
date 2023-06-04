# Django Import
from django.contrib.auth import logout
from django.http import Http404
from django.db import models

# Rest Framework Import
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

# Local Import
from .models import Expense
from .serializers import ExpenseSerializer, RetriveExpenseSerializer


def get_object_or_404(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        raise Http404()


class ExpenseListCreateView(APIView):
    """
    Api View for CRUD of Expenses
    List Expenses
    Create Expenses
    """

    def get_queryset(self):
        user = self.request.user
        return Expense.objects.filter(
            models.Q(creator=user) | models.Q(participants__account=user)
        )

    def get(self, request):
        expenses = self.get_queryset()
        serializer = serializer = RetriveExpenseSerializer(expenses, many=True)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"status": False}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            expense = serializer.save()
            return Response(
                {"expense_id": str(expense.id)},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetriveUpdateExpenseView(APIView):
    """
    View to retrive,update and delete expenses based on id
    """

    def get(self, request, expense_id=None):
        expense = get_object_or_404(Expense, id=expense_id)
        serializer = RetriveExpenseSerializer(expense)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"status": False}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, expense_id=None):
        expense = get_object_or_404(Expense, id=expense_id)
        serializer = ExpenseSerializer(expense, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
