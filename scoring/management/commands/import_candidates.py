import os
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from scoring.models.candidate import Candidate
from scoring.models.question_answer import QuestionAnswer
from utils.cleaning.helpers import clean_text
from utils.scoring.helpers import extract_years_of_experience
from django.utils import timezone


class Command(BaseCommand):
    help = 'Import candidates from a CSV file using pandas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv',
            type=str,
            help='Path to the CSV file containing candidate data',
            default='candidates.csv'
        )

    def handle(self, *args, **options):
        csv_file = options['csv']
        csv_path = str(os.path.join(settings.BASE_DIR, csv_file))

        if not os.path.exists(csv_path):
            raise CommandError(f"CSV file not found at path: {csv_path}")

        self.stdout.write(self.style.SUCCESS(f'Starting import from {csv_path}'))

        try:
            # Read the CSV file using pandas
            df = pd.read_csv(csv_path, encoding='utf-8', header=0,
                             names=["Name", "Job title", "Job department", "Job location", "Headline", "Creation time",
                                    "Stage", "Tags", "Source", "Type", "Summary", "Keywords", "Educations",
                                    "Experiences",
                                    "Skills", "Disqualified", "Disqualified at", "Disqualification category",
                                    "Disqualification reason", "Disqualification note", "Question 1", "Answer 1",
                                    "Question 2", "Answer 2", "Question 3", "Answer 3", "Question 4", "Answer 4",
                                    "Question 5", "Answer 5", "Question 6", "Answer 6", "Question 7", "Answer 7"])

            # Replace NaN with empty strings
            df.fillna('', inplace=True)

            # Convert all string columns to strings and strip whitespace
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

            # Iterate over DataFrame rows
            for index, row in df.iterrows():
                # Convert row to a dictionary
                row_data = row.to_dict()
                print(f"{row_data=}")

                # Clean and preprocess row data
                cleaned_row = {k: str(v).strip() if v else '' for k, v in row_data.items()}

                # Parse creation_time
                creation_time = self.parse_date(cleaned_row.get('Creation time'))
                print(f"{creation_time=}")
                if creation_time is None:
                    self.stdout.write(self.style.WARNING(
                        f'Creation time missing for candidate {cleaned_row.get("Name")}, setting to current time.'
                    ))
                    creation_time = timezone.now()

                # Create or update Candidate
                candidate = Candidate(
                    **{
                        'name': cleaned_row.get('Name', ''),
                        'job_title': cleaned_row.get('Job title', ''),
                        'job_department': cleaned_row.get('Job department', ''),
                        'job_location': cleaned_row.get('Job location', ''),
                        'headline': cleaned_row.get('Headline', ''),
                        'creation_time': creation_time,
                        'stage': cleaned_row.get('Stage', ''),
                        'tags': cleaned_row.get('Tags', ''),
                        'source': cleaned_row.get('Source', ''),
                        'type': cleaned_row.get('Type', ''),
                        'summary': cleaned_row.get('Summary', ''),
                        'keywords': cleaned_row.get('Keywords', ''),
                        'educations': cleaned_row.get('Educations', ''),
                        'experiences': cleaned_row.get('Experiences', ''),
                        'skills': cleaned_row.get('Skills', ''),
                        'disqualified': self.parse_boolean(cleaned_row.get('Disqualified')),
                        'disqualified_at': self.parse_date(cleaned_row.get('Disqualified at')),
                        'disqualification_category': cleaned_row.get('Disqualification category', ''),
                        'disqualification_reason': cleaned_row.get('Disqualification reason', ''),
                        'disqualification_note': cleaned_row.get('Disqualification note', ''),
                    }
                )

                self.stdout.write(f'Created candidate: {candidate.name}')

                # Handle Question and Answers
                for i in range(1, 8):
                    q_field = f'Question {i}'
                    a_field = f'Answer {i}'

                    question_text = cleaned_row.get(q_field, '')
                    answer_text = cleaned_row.get(a_field, '')

                    if question_text:
                        # Clean question and answer
                        question_text = clean_text(question_text)
                        answer_text = clean_text(answer_text)

                        qa, qa_created = QuestionAnswer.objects.update_or_create(
                            candidate=candidate,
                            question=question_text,
                            answer=answer_text
                        )

            self.stdout.write(self.style.SUCCESS('Import completed successfully'))

        except Exception as e:
            raise CommandError(f'Error importing candidates: {e}')

    def parse_date(self, date_str):
        from dateutil import parser
        if date_str and date_str.strip():
            try:
                return parser.parse(date_str)
            except (ValueError, TypeError):
                self.stdout.write(self.style.WARNING(f'Invalid date format: {date_str}'))
        # Return current datetime if date_str is empty or invalid
        return None

    def parse_boolean(self, value):
        if value:
            value = value.lower()
            if value in ['true', '1', 'yes']:
                return True
            elif value in ['false', '0', 'no']:
                return False
        return False
