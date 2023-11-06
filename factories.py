import factory

from trivia_app.models import *


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Category {n}")

    class Meta:
        model = Category


class QuestionTypeFactory(factory.django.DjangoModelFactory):
    question_type = factory.Sequence(lambda n: f"QuestionType {n}?")

    class Meta:
        model = QuestionType


class DifficultyFactory(factory.django.DjangoModelFactory):
    level = factory.Iterator(["easy", "medium", "hard"])

    class Meta:
        model = Difficulty


class QuestionFactory(factory.django.DjangoModelFactory):
    category = factory.SubFactory(CategoryFactory)
    question_type = factory.SubFactory(QuestionTypeFactory)
    difficulty = factory.SubFactory(DifficultyFactory)
    text = factory.Sequence(lambda n: f"Question {n}?")

    class Meta:
        model = Question


class AnswerFactory(factory.django.DjangoModelFactory):
    question = factory.SubFactory(QuestionFactory)
    text = factory.Sequence(lambda n: f"Answer {n}")
    is_correct = False

    class Meta:
        model = Answer
