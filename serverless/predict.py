import os
from typing import List, Dict, Any

from utils.scoring.score_candidate import CandidateRanker


class Predictor:
    """Predictor class to load the model and handle inferences"""

    def setup(self):
        """Load the model and set the device"""
        self.model = CandidateRanker()

    def predict(
            self,
            candidates: List[Dict[str, Any]],
            query: str,
            key_weights: Dict[str, float]
    ):
        """Predict the audio from the text"""
        scores = self.model.rank_candidates(candidates, query, key_weights)
        return scores
