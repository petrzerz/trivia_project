from django.shortcuts import render, get_object_or_404
from .models import Question, Category, Answer

from django.shortcuts import render
from .models import Question, Category


def question_list(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    if selected_category:
        questions = Question.objects.filter(category__name=selected_category)
    else:
        questions = Question.objects.all()
    return render(request, 'question_list.html', {'questions': questions, 'categories': categories})


def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'question_detail.html', {'question': question})
