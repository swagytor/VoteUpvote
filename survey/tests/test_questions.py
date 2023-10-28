from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from survey.models import Survey, Question
from users.models import User


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

        self.question = Question.objects.create(
            survey=self.survey,
            question="What's up?",
            answer="I'm good"
        )

        self.client.force_authenticate(user=self.user)

    def test_get_response_unauthorized(self):
        self.client.force_authenticate()

        response = self.client.post(reverse('surveys:question-create'))

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(reverse('surveys:question-list'))

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(reverse('surveys:question-get', args=[self.question.pk]))

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(reverse('surveys:question-update', args=[self.question.pk]))

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(reverse('surveys:question-delete', args=[self.question.pk]))

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_question(self):
        url = reverse('surveys:question-create')

        post_data = {
            "survey": self.survey.pk,
            "question": "How are you?"
        }

        expected_response = {'pk': 2,
                             'question': 'How are you?',
                             'choices': [],
                             'survey': 1,
                             'answer': None}

        response = self.client.post(url, data=post_data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        self.assertEquals(response.json(), expected_response)

    def test_list_question(self):
        url = reverse('surveys:question-list')

        expected_response = [{'pk': self.question.pk,
                              'question': "What's up?",
                              'choices': [],
                              'answer': "I'm good"}]

        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json(), expected_response)

    def test_retrieve_question(self):
        url = reverse('surveys:question-get', args=[self.question.pk])

        expected_response = {'pk': self.question.pk,
                             'question': "What's up?",
                             'choices': [],
                             'answer': "I'm good"}

        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json(), expected_response)

    def test_update_question_user(self):
        url = reverse('surveys:question-update', args=[self.question.pk])
        new_data = {
            'question': "Changed question?",
            'answer': 'New answer',
        }

        response = self.client.put(url, data=new_data)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_question_owner(self):
        self.client.force_authenticate(user=self.admin)

        url = reverse('surveys:question-update', args=[self.question.pk])
        new_data = {
            'question': "Changed question",
            'answer': 'New answer',
        }

        expected_response = {'pk': self.question.pk,
                             'question': "Changed question",
                             'choices': [],
                             'answer': "New answer"}

        response = self.client.put(url, data=new_data)

        self.assertEquals(response.json(), expected_response)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_delete_question_user(self):
        url = reverse('surveys:question-delete', args=[self.question.pk])

        response = self.client.delete(url)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_question_owner(self):
        self.client.force_authenticate(user=self.admin)

        url = reverse('surveys:question-delete', args=[self.question.pk])
        list_url = reverse('surveys:question-list')

        response = self.client.delete(url)
        list_response = self.client.get(list_url)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(list_response.json(), [])
