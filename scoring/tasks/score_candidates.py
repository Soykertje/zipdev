"""Task to score candidates."""
# Django
from django.conf import settings

# Models
from scoring.models import ScoringTask, Candidate

# Utils
from utils.scoring.score_candidate import CandidateRanker
from utils.scoring.helpers import extract_years_of_experience, map_education_level

# Celery
from zipdev.celery import app


@app.task(bind=True, ignore_result=True, max_retries=5, default_retry_delay=1, queue="score_dandidates")
def score_candidates(self, scoring_task_id: int):
    scoring_task = ScoringTask.objects.get(id=scoring_task_id)
    try:
        scoring_task.status = ScoringTask.StatusChoices.PENDING
        scoring_task.save()
        candidates = list(Candidate.objects.values("id", "experiences", "summary", "skills", "educations"))
        for candidate in candidates:
            candidate["experience_years"] = extract_years_of_experience(candidate["experiences"])
            candidate["education_score"] = map_education_level(candidate["experiences"])

        ranker = CandidateRanker()
        result = ranker.rank_candidates(candidates, scoring_task.query, settings.CANDIDATE_SCORING_WEIGHTS)
        if len(result) > 30:
            result = result[:30]
        result = [{"id": element[0]["id"], "score": round(float(element[1]), 2) * 100} for element in result]
        scoring_task.result = result
    except Exception as e:
        self.retry(exc=e)
        return
    scoring_task.status = ScoringTask.StatusChoices.COMPLETED
    scoring_task.save()
