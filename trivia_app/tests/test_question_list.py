import pytest
from django.test import Client, RequestFactory
from django.urls import reverse, resolve
from factories import CategoryFactory, DifficultyFactory, QuestionFactory, AnswerFactory
from pytest_django.asserts import assertTemplateUsed
from trivia_app.forms import FilterForm
from trivia_app.views import question_list


# Test whether the URL for the question list resolves properly
@pytest.mark.django_db
def test_question_list_url():
    path = reverse('question_list')
    assert resolve(path).view_name == 'question_list'


# Test whether the correct template is used for the question list view
@pytest.mark.django_db
def test_question_list_template():
    test_client = Client()
    url = reverse('question_list')
    response = test_client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'question_list.html')


# Test the question list view by creating test data using factories
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


# Test the question list view with category filtering
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


# Test the question list view with difficulty filtering
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


# Test the validity of the form with valid data
@pytest.mark.django_db
def test_question_list_form_valid():
    category = CategoryFactory.create(name='Category 1')
    difficulty = DifficultyFactory.create(level='Easy')
    form_data = {
        'category': category.name,
        'difficulty': difficulty.level,
        'question_term': 'sample',
    }
    form = FilterForm(data=form_data)
    assert form.is_valid()


# Test the invalidity of the form with invalid data
@pytest.mark.django_db
def test_question_list_form_invalid():
    category = CategoryFactory.create(name='Category 2')
    difficulty = DifficultyFactory.create(level='Medium')
    form_data = {
        'category': category.name,
        'difficulty': difficulty.level,
        'question_term': 'sample' * 50,
    }

    form = FilterForm(data=form_data)
    assert not form.is_valid()
