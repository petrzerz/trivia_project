from django.db.models import Q
from django.shortcuts import render

from .forms import FilterForm
from .models import Question, Category, Difficulty


def question_list(request):
    form = FilterForm(request.GET)
    selected_category = request.GET.get('category')
    selected_difficulty = request.GET.get('difficulty')
    query = Q()
    queryset = Question.objects.all()
    if selected_category:
        query &= Q(category__name=selected_category)
    if selected_difficulty:
        query &= Q(difficulty__level=selected_difficulty)
    questions = queryset.filter(query)
    return render(request, 'question_list.html',
                  {'questions': questions, 'form': form})
