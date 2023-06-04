from django.db import models
import uuid
from django.utils import timezone

# Local Imports
from authentication.models import Account

# Create your models here.


class Expense(models.Model):
    """
    Base Expense Class
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    # Other Basic Data
    total_amount = models.FloatField(default=0)
    payed_back = models.FloatField(default=0)

    def __str__(self):
        return (
            f"{self.name} by {self.creator.primary_identifier} - {self.created_on.date}"
        )


class ExpenseParticipant(models.Model):
    """ """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    expense = models.ForeignKey(
        Expense, on_delete=models.CASCADE, related_name="participants"
    )
    share = models.FloatField(default=0)
    payed_back = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now=True)

    """
    def save(self, *args, **kwargs):
        if not self.id:
            # New instance is being created
            self.timestamp = timezone.now()
        else:
            # Existing instance is being updated
            old_instance = ExpenseParticipant.objects.get(pk=self.id)
            if self.payed_back != old_instance.payed_back:
                self.timestamp = timezone.now()

        super().save(*args, **kwargs)

    """
