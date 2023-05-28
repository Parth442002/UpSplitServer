from rest_framework import serializers


# Local Imports
from authentication.models import Account
from .models import Expense, ExpenseParticipant


class ExpenseParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseParticipant
        fields = ["id", "account", "share", "payed_back"]


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ("id", "name", "creator")
        read_only = ["id", "created_on"]

    def create(self, validated_data):
        # organizer = "9fb9cb82-bdab-4629-93b7-36799cdc69b9"
        invitees_data = validated_data.pop("participants", [])
        creator = validated_data.pop("creator")
        cr = Account.objects.get(id="cb947579-790d-43b6-bc4f-93f62203ed7a")
        meeting = Expense.objects.create(creator=cr, **validated_data)
        # meeting.invitees.set(invitees_data)
        return meeting
