# Django Import
from django.contrib.auth import logout
# Rest Framework Import
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
# Rest Framework JWT Import
from rest_framework_simplejwt.views import TokenObtainPairView

# Local Import
from .models import Account
from .serializers import MyTokenObtainPairSerializer, AccountRegisterSerializer
from .helpers import get_tokens_for_user


#  signin/Login
class AccountLoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Register/SignUp
class AccountRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = AccountRegisterSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            tokens = get_tokens_for_user(account)
            return Response({
                "refresh": tokens['refresh'],
                "access": tokens['access']},
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors["primary_identifier"],
                        status=status.HTTP_400_BAD_REQUEST)
