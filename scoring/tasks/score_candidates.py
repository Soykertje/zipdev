"""Task to score candidates."""
# Django
from django.conf import settings

# Models
from scoring.models import ScoringTask, Candidate

# Utils
import runpod
import time
from utils.scoring.helpers import extract_years_of_experience, map_education_level

# Celery
from zipdev.celery import app


@app.task(bind=True, ignore_result=True, max_retries=5, default_retry_delay=1, queue="score_dandidates")
def score_candidates(self, scoring_task_id: int):
    scoring_task = ScoringTask.objects.get(id=scoring_task_id)
    candidates = list(Candidate.objects.values("id", "experiences", "summary", "skills", "educations"))
    for candidate in candidates:
        candidate["experience_years"] = extract_years_of_experience(candidate["experiences"])
        candidate["education_score"] = map_education_level(candidate["experiences"])
    runpod_api_key = settings.RUNPOD_API_KEY
    runpod.api_key = runpod_api_key
    endpoint_id = settings.SCORER_ENDPOINT_ID
    endpoint = runpod.Endpoint(endpoint_id)
    payload = {
        "input": {
            "query": scoring_task.query,
            "candidates": candidates,
            "key_weights": settings.CANDIDATE_SCORING_WEIGHTS,
        }
    }
    response = endpoint.run(payload)
    while response.status() in ["IN_QUEUE", "IN_PROGRESS"]:
        time.sleep(1)
    if response.status() != "COMPLETED":
        self.retry()
    response = response.output()
    if len(response) > 30:
        result = response[:30]
    result = [{"id": element[0]["id"], "score": round(float(element[1]), 2) * 100} for element in result]
    scoring_task.result = result
    scoring_task.status = ScoringTask.StatusChoices.COMPLETED
    scoring_task.save()
