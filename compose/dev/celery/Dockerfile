FROM python:3.11.8

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY /requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Downloads the NLTK wordnet corpus to avoid downloading it every time the container starts
RUN python -c "import nltk; nltk.download('wordnet')"
# Downloads the model to avoid downloading it every time the container starts
RUN python -c "from sentence_transformers import SentenceTransformer; model_path = '/sentence_transformers/model/'; model = SentenceTransformer('all-MiniLM-L6-v2'); model.save(model_path)"

COPY /compose/dev/celery/worker/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

WORKDIR /app
