"""Service for view scoring_result_detail."""
# Django
from django.shortcuts import render, get_object_or_404

# Models
from scoring.models import ScoringTask, Candidate

from utils.services import BaseService


class ScoringResultDetail(BaseService):

    @staticmethod
    def get_completed_results(lookup_fields, exclude_fields):
        # Extract the list of IDs
        ids = [item['id'] for item in lookup_fields]

        # Query the model for matching IDs
        queryset = Candidate.objects.filter(id__in=ids)

        # Create a mapping of ID to model instance for sorting
        queryset_by_id = {obj.id: obj for obj in queryset}

        # Process and sort results
        sorted_results = []
        for item in lookup_fields:
            obj = queryset_by_id.get(item['id'])
            if obj:
                obj_dict = obj.__dict__.copy()  # Convert model instance to dictionary
                obj_dict.pop('_state', None)  # Remove internal Django state
                obj_dict['score'] = item['score']  # Add the score

                # Filter out excluded fields
                filtered_data = {k: v for k, v in obj_dict.items() if k not in exclude_fields}

                # Reorder dictionary to have 'score' as the first key
                sorted_result = {"score": filtered_data.pop("score"), **filtered_data}
                sorted_results.append(sorted_result)
        return sorted_results

    def execute(self, request, pk: int):
        scoring_task = get_object_or_404(ScoringTask, id=pk)
        if scoring_task.status == ScoringTask.StatusChoices.COMPLETED:
            exclude_fields = ["id", "created_at", "updated_at"]
            sorted_results = self.get_completed_results(scoring_task.result, exclude_fields)
            return render(request, 'scoring/scoring_detail_completed.html',
                          {'query': scoring_task.query, 'result': sorted_results})
        return render(request, 'scoring/scoring_detail_pending.html', {'scoring_task': scoring_task})
