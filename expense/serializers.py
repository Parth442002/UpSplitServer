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
        fields = ["id", "creator", "created_on", "participants"]
        read_only_fields = ["id", "created_on"]

    def create(self, validated_data):
        participants_data = validated_data.pop("participants")
        expense = Expense.objects.create(**validated_data)
        for participant in participants_data:
            import pdb

            pdb.set_trace()
            ExpenseParticipant.objects.create(expense=expense, **participant)
        return expense
