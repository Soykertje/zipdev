import pandas as pd
from datetime import datetime
from scoring.models import Candidate, QuestionAnswer


def import_candidates_from_xlsx(file):
    """
    Imports candidates and their associated question-answers from an XLSX file.
    """
    # Read the Excel file into a Pandas DataFrame
    df = pd.read_excel(file)

    # Initialize lists for bulk creation
    question_answers_to_create = []
    candidates_created = 0

    # Iterate over rows and process data
    for _, row in df.iterrows():
        candidate_data = {
            "name": row["Name"],
            "job_title": row["Job title"],
            "job_department": row["Job department"],
            "job_location": row["Job location"],
            "headline": row.get("Headline"),
            "creation_time": pd.to_datetime(row["Creation time"]),
            "stage": row["Stage"],
            "tags": row.get("Tags"),
            "source": row["Source"],
            "type": row["Type"],
            "summary": row.get("Summary"),
            "keywords": row.get("Keywords"),
            "educations": row.get("Educations"),
            "experiences": row.get("Experiences"),
            "skills": row.get("Skills"),
            "disqualified": bool(row["Disqualified"]),
            "disqualified_at": pd.to_datetime(row["Disqualified at"]) if pd.notna(row["Disqualified at"]) else None,
            "disqualification_category": row.get("Disqualification category"),
            "disqualification_reason": row.get("Disqualification reason"),
            "disqualification_note": row.get("Disqualification note"),
        }

        for key, value in candidate_data.items():
            candidate_data[key] = value.replace('"', "").replace("'", "") if isinstance(value, str) else value

        # Check for duplicate candidates
        candidate, created = Candidate.objects.get_or_create(
            name=candidate_data["name"],
            job_title=candidate_data["job_title"],
            defaults=candidate_data
        )

        if created:
            candidates_created += 1

        # Process question-answer pairs
        for i in range(1, 8):  # Question columns start from "Question 1" to "Question 7"
            question = row.get(f"Question {i}")
            answer = row.get(f"Answer {i}")
            if pd.notna(question):
                if not QuestionAnswer.objects.filter(candidate=candidate, question=question).exists():
                    question_answers_to_create.append(
                        QuestionAnswer(candidate=candidate, question=question, answer=answer)
                    )

    # Bulk create question answers
    QuestionAnswer.objects.bulk_create(question_answers_to_create)

    return candidates_created
