from rest_framework import serializers


# Local Imports
from authentication.models import Account
from .models import Expense, ExpenseParticipant


class ExpenseParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseParticipant
        fields = ["id", "account", "share", "payed_back"]


class ExpenseSerializer(serializers.ModelSerializer):
    participants = ExpenseParticipantSerializer(
        many=True,
    )

    class Meta:
        model = Expense
        fields = (
            "id",
            "name",
            "creator",
            "participants",
            "total_amount",
            "payed_back",
            "created_on",
        )
        read_only = ["id", "created_on"]

    def create(self, validated_data):
        participants = validated_data.pop("participants")
        # Creating Expense Object
        expense = Expense.objects.create(**validated_data)
        # Create Expense Participants
        for participant in participants:
            ExpenseParticipant.objects.create(expense=expense, **participant)

        return expense

    def update(self, instance, validated_data):
        participants = validated_data.get("participants", None)
        # If Participants are not provided
        if participants == None:
            for field, value in validated_data.items():
                setattr(instance, field, value)
        # If participants are provided:-
        else:
            # Creating or updating participant Objects
            participants = validated_data.pop("participants")
            for participant_data in participants:
                account = participant_data.pop("account")

                participant, created = ExpenseParticipant.objects.update_or_create(
                    expense=instance, account=account, **participant_data
                )
                participant = ExpenseParticipant.objects.get(
                    expense=instance,
                    account=account,
                )
                if created:
                    print("new instance created")
                else:
                    print("last instance updated")

                participant.save()

        instance.save()
        return instance


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
