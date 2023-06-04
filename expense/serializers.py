from rest_framework import serializers


# Local Imports
from authentication.models import Account
from .models import Expense, ExpenseParticipant


class ExpenseParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseParticipant
        fields = ["id", "account", "share", "payed_back"]


class ExpenseSerializer(serializers.ModelSerializer):
    participants = ExpenseParticipantSerializer(many=True)

    class Meta:
        model = Expense
        fields = ("id", "name", "creator", "participants", "total_amount", "payed_back")
        read_only = ["id", "created_on"]

    def create(self, validated_data):
        participants = validated_data.pop("participants")
        # Creating Expense Object
        expense = Expense.objects.create(**validated_data)
        # Create Expense Participants
        for participant in participants:
            ExpenseParticipant.objects.create(expense=expense, **participant)

        return expense


class RetriveExpenseSerializer(serializers.ModelSerializer):
    participants = ExpenseParticipantSerializer(many=True)

    class Meta:
        model = Expense
        fields = (
            "id",
            "name",
            "creator",
            "created_on",
            "total_amount",
            "payed_back",
            "participants",
        )
        read_only = ["id", "created_on"]
