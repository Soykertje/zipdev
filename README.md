# Zipdev Assessment 

You can find the deployed project at https://zipdev.jangom.com

This solution is built using Djangp + Celery

The decision to use Django was made because of the ease of use and the fact that it is a full stack framework, 
which allowed me to not worry about working in an entire frontend project. 
Celery was used to handle the background tasks scoring candidates.
The actual scoring algorithm runs in Runpod under a serverless architecture, so running this project in local completely
is not possible unless you have access to the Runpod API. Or you decide to make the 
changes to run the socring algorithm in local.

The scoring algorithm is located at `utils/scoring/score_candidate.py` and it's made
framework-agnostic, so it can be used in any project.

To effectively run the project, you must create two files:
### .env/.local/.django
```bash
DJANGO_SECRET_KEY="django_secret_key"
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS="localhost .localhost *"
DJANGO_CSRF_TRUSTED_ORIGINS="http://* https://*"
ALLOWED_CORS_SOURCES = "http://* https://*"
RUNPOD_API_KEY="runpod_api_key"
SCORER_ENDPOINT_ID="runpod_endpoint_id"
```

### .env/.local/.postgres
```bash
export POSTGRES_USER=zipdev
export POSTGRES_DB=zipdev
export POSTGRES_PASSWORD=zipdev
export POSTGRES_HOST=postgres
export POSTGRES_PORT=5432
```

And then run the following commands:
```bash
docker compose -f compose.local.yml build
docker compose -f compose.local.yml up
```

After all the containers are up and running, visit http://localhost

