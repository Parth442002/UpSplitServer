# Django Import
from django.contrib.auth import logout

# Rest Framework Import
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

# Local Import
from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseListCreateView(APIView):
    """
    Api View for CRUD of Expenses
    List Expenses
    Create Expenses
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        raise NotImplementedError("This function has not been implemented")

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {status: "Expense Created"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
