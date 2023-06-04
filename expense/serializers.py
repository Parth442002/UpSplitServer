from rest_framework import serializers


# Local Imports
from authentication.models import Account
from .models import Expense, ExpenseParticipant


class ExpenseParticipantSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()

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
        participants = validated_data.pop("participants")
        for field, value in validated_data.items():
            setattr(instance, field, value)
        # handling the participants
        for participant_data in participants:
            participant_id = participant_data.get("id", None)
            import pdb

            pdb.set_trace()
            # If we want to edit an existing participant
            if participant_id != None:
                participant = ExpenseParticipant.objects.get(id=participant_id)
                for field, value in participant_data.items():
                    setattr(participant, field, value)
                participant.save()
            if not participant_id:
                # If we want to add a new participant
                participant = ExpenseParticipant.objects.create(
                    expense=instance, **participant_data
                )
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
