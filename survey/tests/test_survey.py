import datetime
import pprint

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from survey.models import Survey, Question, Choice
from users.models import User


# Create your tests here.
class SurveyTestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin',
            first_name='IT',
            last_name='Power',
            password='12345'
        )

        self.user = User.objects.create_user(
            username='user',
            first_name='Alex',
            last_name='Ignatenko',
            password='12345'
        )

        self.survey = Survey.objects.create(
            title='API TestCase',
            description='Description for TestCase',
            author=self.admin,
        )

        self.first_question = Question.objects.create(
            survey=self.survey,
            question="What's up?",
            answer="I'm good"
        )
        self.second_question = Question.objects.create(
            survey=self.survey,
            question="Tell me about yourself"
        )

        self.first_option = Choice.objects.create(
            question=self.second_question,
            option="My name is Yoshikage Kira. I'm 33 years old..."
        )
        self.second_option = Choice.objects.create(
            question=self.second_question,
            option="My name is Jeff")

        self.client.force_authenticate(user=self.user)

    def test_get_response_unauthorized(self):
        self.client.force_authenticate()

        response = self.client.post(reverse('surveys:survey-list'))

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(reverse('surveys:survey-list'))

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(reverse('surveys:survey-detail', args=[self.survey.pk]))

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(reverse('surveys:survey-detail', args=[self.survey.pk]))

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(reverse('surveys:survey-detail', args=[self.survey.pk]))

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_survey(self):
        self.maxDiff = None

        post_url = reverse('surveys:survey-list')

        post_data = {
            "title": "Насколько вы хороши в программировании?",
            "description": "Сможете ли ответить на вопросы как настоящий программист?",
            "questions": [{
                "question": "Опишите путь программиста",
                "choices": [
                    {
                        "option": "Через костыли к багам"
                    },
                    {
                        "option": "Мастер по набиванию шишек"
                    },
                    {
                        "option": "Постоянно учиться чему-то новому"
                    }
                ]
            }
            ]
        }

        response = self.client.post(post_url, data=post_data, format='json')

        expected_response = {'pk': response.json().get('pk'),
                             'title': 'Насколько вы хороши в программировании?',
                             'description': 'Сможете ли ответить на вопросы как настоящий программист?',
                             'questions': [{'pk': response.json()['questions'][0].get('pk'),
                                            'question': 'Опишите путь программиста',
                                            'choices': [{'option': 'Через костыли к багам'},
                                                        {'option': 'Мастер по набиванию шишек'},
                                                        {'option': 'Постоянно учиться чему-то новому'}],
                                            'answer': None}],
                             'likes_count': 0,
                             'views_count': 0,
                             'published_at': datetime.date.today().isoformat(),
                             'author': self.user.pk}

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        self.assertEquals(response.json(), expected_response)

    def test_get_survey_list(self):
        url = reverse('surveys:survey-list')
        expected_response = [{
            'title': 'API TestCase',
            'id': self.survey.pk,
            'description': 'Description for TestCase',
            'is_watched': False,
            'likes_count': 0,
            'views_count': 0
        }]

        response = self.client.get(url)

        self.assertEquals(response.json(), expected_response)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_survey_retrieve_and_is_watched_status(self):
        self.maxDiff = None

        url = reverse('surveys:survey-detail', args=[self.survey.pk])

        expected_response = {'pk': self.survey.pk,
                             'title': 'API TestCase',
                             'description': 'Description for TestCase',
                             'questions': [{'pk': self.first_question.pk,
                                            'question': "What's up?",
                                            'choices': [],
                                            'answer': "I'm good"},
                                           {'pk': self.second_question.pk,
                                            'question': 'Tell me about yourself',
                                            'choices': [{
                                                'option': "My name is Yoshikage Kira. I'm 33 "
                                                          'years old...'},
                                                {'option': 'My name is Jeff'}],
                                            'answer': None}],
                             'likes_count': 0,
                             'views_count': 1,
                             'published_at': datetime.date.today().isoformat(),
                             'author': self.admin.pk}

        response = self.client.get(url)

        self.assertEquals(response.json(), expected_response)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_update_survey_user(self):
        update_url = reverse('surveys:survey-detail', args=[self.survey.pk])
        new_data = {
            'title': 'API TestCase',
            'description': 'Updated description',
        }

        response = self.client.put(update_url, data=new_data)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_survey_owner(self):
        self.client.force_authenticate(user=self.admin)

        update_url = reverse('surveys:survey-detail', args=[self.survey.pk])
        list_url = reverse('surveys:survey-list')

        expected_response = [{
            'title': 'API TestCase',
            'id': self.survey.pk,
            'description': 'Updated description',
            'is_watched': False,
            'likes_count': 0,
            'views_count': 0
        }]

        new_data = {
            'title': 'API TestCase',
            'description': 'Updated description',
        }

        response = self.client.put(update_url, data=new_data)

        list_response = self.client.get(list_url)

        self.assertEquals(list_response.json(), expected_response)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_delete_survey_user(self):
        delete_url = reverse('surveys:survey-detail', args=[self.survey.pk])

        response = self.client.delete(delete_url)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_survey_owner(self):
        self.client.force_authenticate(user=self.admin)

        delete_url = reverse('surveys:survey-detail', args=[self.survey.pk])
        list_url = reverse('surveys:survey-list')

        response = self.client.delete(delete_url)
        list_response = self.client.get(list_url)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(list_response.json(), [])

    def test_like_survey_and_is_watched_status(self):
        retrieve_url = reverse('surveys:survey-detail', args=[self.survey.pk])
        like_url = reverse('surveys:survey-like', args=[self.survey.pk])
        favorite_url = reverse('surveys:survey-favorite')

        # пробуем поставить лайк на непросмотренный опрос
        like_response = self.client.get(like_url)

        self.assertEquals(like_response.json(), {'error': 'Вы не можете поставить оценку так как не посмотрели опрос!'})

        # отправляем запрос на просмотр опроса
        retrieve_response = self.client.get(retrieve_url)

        # после просмотра флаг is_watched становится True, а также появляется возможность ставить оценки опросам
        like_response = self.client.get(like_url)

        self.assertEquals(like_response.status_code, status.HTTP_200_OK)

        response = self.client.get(favorite_url)

        expected_response = [{'id': response.json()[0].get('id'),
                              'survey': {'description': 'Description for TestCase',
                                         'id': self.survey.pk,
                                         'is_watched': True,
                                         'likes_count': 1,
                                         'title': 'API TestCase',
                                         'views_count': 1}}]

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(response.json(), expected_response)

    def test_dislike_survey(self):
        dislike_url = reverse('surveys:survey-dislike', args=[self.survey.pk])
        retrieve_url = reverse('surveys:survey-detail', args=[self.survey.pk])

        # пробуем поставить дизлайк на непросмотренный опрос
        like_response = self.client.get(dislike_url)

        self.assertEquals(like_response.json(), {'error': 'Вы не можете поставить оценку так как не посмотрели опрос!'})

        # отправляем запрос на просмотр опроса
        retrieve_response = self.client.get(retrieve_url)

        # после просмотра появляется возможность ставить оценки опросам
        like_response = self.client.get(dislike_url)

        self.assertEquals(like_response.status_code, status.HTTP_200_OK)

    def test_history(self):
        history_url = reverse('surveys:survey-history')
        retrieve_url = reverse('surveys:survey-detail', args=[self.survey.pk])

        history_response = self.client.get(history_url)

        self.assertEquals(history_response.status_code, status.HTTP_200_OK)

        self.assertEquals(history_response.json(), [])

        retrieve_response = self.client.get(retrieve_url)
        self.assertEquals(retrieve_response.status_code, status.HTTP_200_OK)

        history_response = self.client.get(history_url)

        expected_response = [{'id': history_response.json()[0].get('id'),
                              'survey': {'description': 'Description for TestCase',
                                         'id': self.survey.pk,
                                         'is_watched': True,
                                         'likes_count': 0,
                                         'title': 'API TestCase',
                                         'views_count': 1}}]

        self.assertEquals(history_response.json(), expected_response)

    def test_my_surveys(self):
        my_surveys_url = reverse('surveys:my-survey')

        expected_response = [{
            'description': 'Description for TestCase',
            'id': self.survey.pk,
            'is_watched': False,
            'likes_count': 0,
            'title': 'API TestCase',
            'views_count': 0}]

        response = self.client.get(my_surveys_url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json(), [])

        self.client.force_authenticate(user=self.admin)

        response = self.client.get(my_surveys_url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json(), expected_response)
