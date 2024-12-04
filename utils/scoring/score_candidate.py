import os
from sklearn.preprocessing import MinMaxScaler
from sentence_transformers import SentenceTransformer, util
from nltk.corpus import wordnet
import numpy as np


class CandidateRanker:
    """
    A class to rank candidates based on textual criteria.
    """

    def __init__(self, model_name='all-MiniLM-L6-v2', model_path='/sentence_transformers/model/'):
        """
        Initialize the CandidateRanker with a pre-trained model.
        Downloads the model if not already present.
        """
        self.model = self._load_model(model_name, model_path)

    @classmethod
    def _load_model(cls, model_name, model_path):
        """
        Load the SentenceTransformer model, downloading it if necessary.
        :param model_name: Name of the SentenceTransformer model.
        :param model_path: Path to save the model.
        :return: SentenceTransformer model.
        """
        os.makedirs(model_path, exist_ok=True)
        model_file_path = str(os.path.join(model_path, model_name))
        if not os.path.exists(model_file_path):
            model = SentenceTransformer(model_name)
            model.save(model_file_path)
        else:
            model = SentenceTransformer(model_file_path)
        return model

    @staticmethod
    def enrich_query(query):
        """
        Expand the query by adding synonyms using WordNet.
        :param query: Query string.
        :return: Enriched query string.
        """
        enriched_query = query
        for word in query.split():
            synonyms = wordnet.synsets(word)
            enriched_query += " " + " ".join([syn.lemma_names()[0] for syn in synonyms])
        return enriched_query

    def compute_similarity_score(self, key_texts, query):
        """
        Compute cosine similarity scores between a list of texts and the query.
        :param key_texts: List of texts to compare.
        :param query: Query text.
        :return: List of similarity scores.
        """
        key_embeddings = self.model.encode(key_texts, convert_to_tensor=True)
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        return util.cos_sim(query_embedding, key_embeddings).numpy().flatten()

    @staticmethod
    def normalize_values(values):
        """
        Normalize a list of numeric values to a scale of 0 to 1.
        :param values: List of numeric values.
        :return: List of normalized values.
        """
        scaler = MinMaxScaler()
        return scaler.fit_transform(np.array(values).reshape(-1, 1)).flatten()

    def rank_candidates(self, candidates, query, key_weights):
        """
        Rank candidates based on a query, their data, and predefined key weights.
        :param candidates: List of candidate dictionaries.
        :param query: Query string.
        :param key_weights: Dictionary of weights for different keys.
        :return: List of ranked candidates with scores.
        """
        # Enrich the query
        enriched_query = self.enrich_query(query)

        # Prepare candidate data for each key
        experience_years = [candidate.get("experience_years", 0) for candidate in candidates]
        education_scores = [candidate.get("education_score", 0) for candidate in candidates]
        normalized_experience_years = self.normalize_values(experience_years)
        normalized_education_scores = self.normalize_values(education_scores)

        # Compute similarity scores for textual keys
        experience_texts = [candidate["experiences"] for candidate in candidates]
        summary_texts = [candidate["summary"] for candidate in candidates]
        skills_texts = [candidate.get("skills", "") for candidate in candidates]
        education_texts = [candidate.get("educations", "") for candidate in candidates]

        experience_scores = self.compute_similarity_score(experience_texts, enriched_query)
        summary_scores = self.compute_similarity_score(summary_texts, enriched_query)
        skills_scores = self.compute_similarity_score(skills_texts, enriched_query)
        education_scores = self.compute_similarity_score(education_texts, enriched_query)

        # Compute final weighted scores
        final_scores = [
            key_weights["experiences"] * exp_score +
            key_weights["summary"] * sum_score +
            key_weights["skills"] * skill_score +
            key_weights["educations"] * edu_score +
            key_weights["experience_years"] * norm_exp_year +
            key_weights["education_score"] * norm_edu_score
            for exp_score, sum_score, skill_score, edu_score, norm_exp_year, norm_edu_score in
            zip(experience_scores, summary_scores, skills_scores, education_scores, normalized_experience_years,
                normalized_education_scores)
        ]

        # Rank candidates by scores
        ranked_candidates = sorted(
            zip(candidates, final_scores), key=lambda x: x[1], reverse=True
        )
        return ranked_candidates
