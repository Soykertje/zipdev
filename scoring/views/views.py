"""Scoring views."""
# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

# Models
from scoring.models import ScoringTask

# Forms
from scoring.forms.scoring_form import ScoringForm
from scoring.forms.import_data_form import ImportDataForm

# Tasks
from scoring.tasks.score_candidates import score_candidates

# Services
from scoring.services.scoring_result_detail import ScoringResultDetail

# Utils
from utils.import_candidates import import_candidates_from_xlsx


def scoring_view(request):
    if request.method == 'POST':
        form = ScoringForm(request.POST)
        if form.is_valid():
            new_scoring_task = ScoringTask.objects.create(query=form.cleaned_data['query'])
            score_candidates.apply_async(args=(new_scoring_task.pk,))
            return redirect('scoring_task_detail', pk=new_scoring_task.pk)
        else:
            return render(request, 'scoring/scoring_form.html', {'form': form})
    else:
        form = ScoringForm()
        return render(request, 'scoring/scoring_form.html', {'form': form})


def scoring_result_list(request):
    # Fetch all ScoringResult objects
    scoring_results = ScoringTask.objects.all()
    return render(request, 'scoring/scoring_list.html', {'scoring_results': scoring_results})


def scoring_result_detail(request, pk: int):
    return ScoringResultDetail().execute(request, pk)


def scoring_result_detail_api(request, pk: int):
    scoring_task = get_object_or_404(ScoringTask, pk=pk)
    return JsonResponse({'status': scoring_task.status})


def import_candidates(request):
    if request.method == 'POST':
        form = ImportDataForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            import_candidates_from_xlsx(file)
            return redirect('home')
        else:
            return render(request, 'import/import_candidates.html', {'form': form})
    else:
        form = ImportDataForm()
        return render(request, 'import/import_candidates.html', {'form': form})

