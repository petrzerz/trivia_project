import os

import django
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "trivia.settings")
django.setup()
from trivia_app.models import Category, QuestionType, Difficulty, Question, Answer

API_URL = 'https://opentdb.com/api.php?amount=20'

response = requests.get(API_URL).json()
print(response)

results = response['results']

for result in results:
    category = Category.objects.get_or_create(name=result['category'])
    question_type = QuestionType.objects.get_or_create(question_type=result['type'])
    difficulty = Difficulty.objects.get_or_create(level=result['difficulty'])
    question = Question.objects.get_or_create(category=category[0], question_type=question_type[0],
                                              difficulty=difficulty[0],
                                              text=result['question'])
    Answer.objects.get_or_create(question=question[0], text=result['correct_answer'], is_correct=True)
    for incorrect_answer in result['incorrect_answers']:
        Answer.objects.get_or_create(question=question[0], text=incorrect_answer, is_correct=False)
