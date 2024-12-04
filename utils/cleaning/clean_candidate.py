"""Util to clean candidate data."""
import re
from datetime import datetime
import pandas as pd
import numpy as np

# For NLP preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Utils
from utils.cleaning.helpers import clean_text, clean_date, clean_boolean


def clean_candidate_data(candidate):
    candidate.name = clean_text(candidate.name)
    candidate.job_title = clean_text(candidate.job_title)
    candidate.job_department = clean_text(candidate.job_department)
    candidate.job_location = clean_text(candidate.job_location)
    candidate.headline = clean_text(candidate.headline)
    candidate.creation_time = clean_date(candidate.creation_time)
    candidate.stage = clean_text(candidate.stage)
    candidate.tags = clean_text(candidate.tags)
    candidate.source = clean_text(candidate.source)
    candidate.type = clean_text(candidate.type)
    candidate.summary = clean_text(candidate.summary)
    candidate.keywords = clean_text(candidate.keywords)
    candidate.educations = clean_text(candidate.educations)
    candidate.experiences = clean_text(candidate.experiences)
    candidate.skills = clean_text(candidate.skills)
    candidate.disqualified = clean_boolean(candidate.disqualified)
    candidate.disqualified_at = clean_date(candidate.disqualified_at)
    candidate.disqualification_category = clean_text(candidate.disqualification_category)
    candidate.disqualification_reason = clean_text(candidate.disqualification_reason)
    candidate.disqualification_note = clean_text(candidate.disqualification_note)
    # Save cleaned data back to the database if necessary
    # candidate.save()
    return candidate
