import pytest
from django.test import Client, RequestFactory
from django.urls import reverse, resolve
from factories import CategoryFactory, DifficultyFactory, QuestionFactory, AnswerFactory
from pytest_django.asserts import assertTemplateUsed
from trivia_app.views import question_list


@pytest.mark.django_db
def test_question_list_url():
    path = reverse('question_list')
    assert resolve(path).view_name == 'question_list'


@pytest.mark.django_db
def test_question_list_template():
    test_client = Client()
    url = reverse('question_list')
    response = test_client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'question_list.html')


@pytest.mark.django_db
def test_question_list_view():
    CategoryFactory.create_batch(5)
    DifficultyFactory.create_batch(3)
    for _ in range(10):
        question = QuestionFactory()
        AnswerFactory.create_batch(4, question=question)

    request = RequestFactory().get("/")
    response = question_list(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_question_list_with_category_filter():
    category = CategoryFactory(name='Test Category')
    other_category = CategoryFactory(name='Other Category')
    difficulty = DifficultyFactory(level='Easy')
    question1 = QuestionFactory(category=category, difficulty=difficulty, text='Question 1')
    question2 = QuestionFactory(category=other_category, difficulty=difficulty, text='Question 2')

    factory = RequestFactory()
    request = factory.get(reverse('question_list'), {'category': category.name})

    response = question_list(request)

    assert response.status_code == 200
    content = response.content.decode('utf-8')

    assert str(question1.text) in content
    assert str(question2.text) not in content


@pytest.mark.django_db
def test_question_list_with_difficulty_filter():
    difficulty = DifficultyFactory(level='Easy')
    other_difficulty = DifficultyFactory(level='Hard')
    category = CategoryFactory(name='Category 1')
    question1 = QuestionFactory(category=category, difficulty=difficulty, text='Question 1')
    question2 = QuestionFactory(category=category, difficulty=other_difficulty, text='Question 2')

    factory = RequestFactory()
    request = factory.get(reverse('question_list'), {'difficulty': difficulty.level})

    response = question_list(request)

    assert response.status_code == 200
    content = response.content.decode('utf-8')

    assert str(question1.text) in content
    assert str(question2.text) not in content
