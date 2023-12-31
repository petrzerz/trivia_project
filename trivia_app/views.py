from django.db.models import Q
from django.shortcuts import render, redirect

from .forms import FilterForm
from .models import Question


def question_list(request):
    form = FilterForm(request.GET)
    selected_category = request.GET.get('category')
    selected_difficulty = request.GET.get('difficulty')
    selected_question_term = request.GET.get('question_term')
    query = Q()
    queryset = Question.objects.all()
    if selected_category:
        query &= Q(category__name=selected_category)
    if selected_difficulty:
        query &= Q(difficulty__level=selected_difficulty)
    if selected_question_term:
        query &= Q(text__icontains=selected_question_term)
    questions = queryset.filter(query)
    if 'clear' in request.GET:
        return redirect('question_list')
    return render(request, 'question_list.html',
                  {'questions': questions, 'form': form})
