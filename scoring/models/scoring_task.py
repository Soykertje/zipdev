"""ScoringTask used to store the scoring task information."""
# Django
from django.db import models

# Utils
from utils.models import BaseModel


class ScoringTask(BaseModel):
    """ScoringTask model."""

    class StatusChoices(models.TextChoices):
        """Status choices."""
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'

    status = models.CharField(choices=StatusChoices.choices, default=StatusChoices.PENDING, max_length=20)
    result = models.JSONField(null=True, blank=True)
    query = models.TextField()
