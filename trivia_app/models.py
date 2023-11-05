from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.id}, {self.name}'


class QuestionType(models.Model):
    question_type = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.id}, {self.question_type}'


class Difficulty(models.Model):
    level = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.id}, {self.level}'


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_questions')
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE, related_name='question_type_questions')
    difficulty = models.ForeignKey(Difficulty, on_delete=models.CASCADE, related_name='difficulty_level_questions')
    text = models.TextField()

    def __str__(self):
        return f'{self.id}, {self.text}'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField()

    def __str__(self):
        return f'{self.id}, {self.text}'
