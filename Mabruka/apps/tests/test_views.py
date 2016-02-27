from django.test import TestCase
from django.test.client import RequestFactory
# Create your tests here.
"""
from apps.users.models import User
from apps.home.views import IndexView
from apps.discuss.models import Questions

class TestHome(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='Jean', email='jean@hotmail.com')
        for i in range(21):
            Question.objects.create(user=self.user, title='pregunta%s' % i, description = 'descripcion')

    def text_viewIndexView(self):
        request =  self.factory.get('/')
        view = IndexView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.response.template_name[0], 'home/index.html')
        self.assertEqual(len(response.context_data['object_list']), 21)
"""
