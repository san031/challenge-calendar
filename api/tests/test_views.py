import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

@pytest.mark.django_db
def test_get_todo_list():
    User = get_user_model()
    user = User.objects.create_user(email='testuser@gmail.com', password='testpass123')

    client = APIClient()
    client.force_authenticate(user=user)  # simulates a logged-in user, skips real login

    response = client.get('/gettodo/')
    assert response.status_code == 200