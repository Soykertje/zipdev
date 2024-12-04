"""Candidate model, stores the relevant information about a candidate."""
# Django
from django.db import models

# Utils
from utils.models import BaseModel


class Candidate(BaseModel):
    name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    job_department = models.CharField(max_length=255)
    job_location = models.CharField(max_length=255)
    headline = models.CharField(max_length=255, blank=True, null=True)
    creation_time = models.DateTimeField()
    stage = models.CharField(max_length=255)
    tags = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    summary = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    educations = models.TextField(blank=True, null=True)
    experiences = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    disqualified = models.BooleanField(default=False)
    disqualified_at = models.DateTimeField(blank=True, null=True)
    disqualification_category = models.CharField(max_length=255, blank=True, null=True)
    disqualification_reason = models.CharField(max_length=255, blank=True, null=True)
    disqualification_note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.pk}"
