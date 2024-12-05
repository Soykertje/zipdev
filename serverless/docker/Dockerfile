
FROM runpod/base:0.6.2-cuda12.1.0

# --- Optional: System dependencies ---
COPY serverless/docker/setup.sh /setup.sh
RUN /bin/bash /setup.sh && \
    rm /setup.sh


# Python dependencies
COPY ./requirements.extra.txt /requirements.txt
RUN python3.11 -m pip install --upgrade pip && \
    python3.11 -m pip install --upgrade -r /requirements.txt --no-cache-dir && \
    rm /requirements.txt
RUN python3.11 -m pip install runpod==1.7.5
RUN python3.11 -m pip install hf-transfer==0.1.8

# Downloads the NLTK wordnet corpus to avoid downloading it every time the container starts
RUN python3.11 -c "import nltk; nltk.download('wordnet')"
# Downloads the model to avoid downloading it every time the container starts
RUN python3.11 -c "from sentence_transformers import SentenceTransformer; model_path = '/sentence_transformers/model/'; model = SentenceTransformer('all-MiniLM-L6-v2'); model.save(model_path)"

COPY ./serverless /serverless/
COPY ./utils/scoring /utils/scoring/
COPY ./handler.py /handler.py
CMD python3.11 -u handler.py
