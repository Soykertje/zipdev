# zipdev
Take Home Project

aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 199254322281.dkr.ecr.us-east-2.amazonaws.com
docker build -t zipdev/django -f compose/dev/django/Dockerfile .
docker tag zipdev/django:latest 199254322281.dkr.ecr.us-east-2.amazonaws.com/zipdev/django:latest
docker push 199254322281.dkr.ecr.us-east-2.amazonaws.com/zipdev/django:latest

docker build -t zipdev/celery -f compose/dev/celery/Dockerfile .
docker tag zipdev/celery:latest 199254322281.dkr.ecr.us-east-2.amazonaws.com/zipdev/celery:latest
docker push 199254322281.dkr.ecr.us-east-2.amazonaws.com/zipdev/celery:latest
