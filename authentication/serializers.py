from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Account


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token["primary_identifier"] = user.primary_identifier
        return token


class AccountRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        # validators=[validate_password]
    )

    class Meta:
        model = Account
        fields = (
            "primary_identifier",
            "password",
        )

    def validate(self, attrs):
        # Validation Logic
        return attrs

    def create(self, validated_data):
        user = Account.objects.create(
            primary_identifier=validated_data["primary_identifier"],
        )
        # setting the user password
        user.set_password(validated_data["password"])
        user.save()

        return user


class AccountViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("id", "primary_identifier")
