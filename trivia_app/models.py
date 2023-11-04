from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)


class QuestionType(models.Model):
    question_type = models.CharField(max_length=255)


class Difficulty(models.Model):
    level = models.CharField(max_length=255)


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_questions')
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE, related_name='question_type_questions')
    difficulty = models.ForeignKey(Difficulty, on_delete=models.CASCADE, related_name='difficulty_level_questions')
    text = models.TextField()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField()
