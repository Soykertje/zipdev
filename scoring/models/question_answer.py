"""QuestionAnswer model for storing the questions asked as well as the answers given by the candidates."""
# Django
from django.db import models

# Models
from scoring.models.candidate import Candidate

# Utils
from utils.models import BaseModel


class QuestionAnswer(BaseModel):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='question_answers')
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Question for {self.candidate.name}'
