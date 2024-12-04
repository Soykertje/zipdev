from django.contrib import admin

from scoring.models import Candidate, QuestionAnswer, ScoringTask


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Candidate._meta.fields]


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in QuestionAnswer._meta.fields]


@admin.register(ScoringTask)
class ScoringTaskAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ScoringTask._meta.fields]
