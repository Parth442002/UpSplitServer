from django.db import models
import uuid
from authentication.models import Account

# Create your models here.


class ExpenseGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=200,
    )
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
