from django.shortcuts import render, get_object_or_404

from django.shortcuts import render
from .models import Question, Category
import random


def question_list(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    if selected_category:
        questions = Question.objects.filter(category__name=selected_category)
    else:
        questions = Question.objects.all()
    return render(request, 'question_list.html', {'questions': questions, 'categories': categories})
