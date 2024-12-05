''' handler.py for runpod worker '''
from serverless.predict import Predictor
import runpod
from runpod.serverless.utils.rp_validator import validate

from serverless.schema import INPUT_SCHEMA

MODEL = Predictor()
MODEL.setup()


def run(job):
    """
    Run inference on the model.
    """
    job_input = job['input']

    # Input validation
    validated_input = validate(job_input, INPUT_SCHEMA)
    #
    if 'errors' in validated_input:
        return {"error": validated_input['errors']}
    candidates = list(job_input.get("candidates", []))
    query = str(job_input.get("query", ""))
    key_weights = dict(job_input.get("key_weights", {}))
    scores = MODEL.predict(
        candidates,
        query,
        key_weights,
    )

    return scores


runpod.serverless.start({"handler": run})
