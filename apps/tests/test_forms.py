from django.test import TestCase

# Create your tests here.
"""
from apps.users.models import User
from apps.discuss.models import Question, Answer


class TestDiscuss(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="JeanCarlos", email = 'jean@hotmail.com', password='jeancarlos')
        self.question = Question.objects.create(user=self.user, titulo='titulo', description='descripcion')

    def text_createAnswer(self):
        user = self.client.login(username='JeanCarlos', password='jeancarlos')
        self.assertTrue(user)
        self.assertEqual(Answer.objects.count(), 0)
        data = {
            'user': self.user.id,
            'question': self.question.id,
            'description': 'asdfagasdfs'
        }
        self.client.post('/pregunta/%s/' & self.question.slug, data)
        self.assertEqual(Answer.objects.count(), 1)
"""
