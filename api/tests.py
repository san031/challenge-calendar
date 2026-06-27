from datetime import date

from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from account.models import User
from api.models import ItemTodo, Todo
from api.views import streakHistoryView


class StreakHistoryViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(email='tester@example.com', password='secret123')
        self.view = streakHistoryView.as_view({'get': 'get'})

    def test_returns_todo_history_when_no_streak_records_exist(self):
        todo = Todo.objects.create(user=self.user, created_at=date.today())
        ItemTodo.objects.create(items=todo, title='Water crops', is_done=True)
        ItemTodo.objects.create(items=todo, title='Check soil', is_done=False)

        request = self.factory.get('/api/streak/history/')
        force_authenticate(request, user=self.user)

        response = self.view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['dateid'], str(date.today()))
        self.assertEqual(response.data[0]['completion_percentage'], 50.0)
