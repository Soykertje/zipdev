"""Form to import data out of a xlsx file."""
from django import forms
import pandas as pd


class ImportDataForm(forms.Form):
    file = forms.FileField(label='File to import', required=True)

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith('.xlsx'):
            raise forms.ValidationError('Invalid file type. Please upload a .xlsx file.')
        expected_headers = [
            "Name", "Job title", "Job department", "Job location", "Headline", "Creation time",
            "Stage", "Tags", "Source", "Type", "Summary", "Keywords", "Educations", "Experiences",
            "Skills", "Disqualified", "Disqualified at", "Disqualification category",
            "Disqualification reason", "Disqualification note", "Question 1", "Answer 1",
            "Question 2", "Answer 2", "Question 3", "Answer 3", "Question 4", "Answer 4",
            "Question 5", "Answer 5", "Question 6", "Answer 6", "Question 7", "Answer 7"
        ]
        df = pd.read_excel(file)
        if list(df.columns) != expected_headers:
            raise forms.ValidationError('Invalid file format. Please upload a file with the correct headers.')
        return file
