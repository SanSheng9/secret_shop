import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserTestCase(APITestCase):
    profile_list_url = reverse('all-profiles')

    def setUp(self):
        # Новый юзер
        data = json.dumps({
            "username": "testuser",
            "password": "oral1234"
        })
        self.user = self.client.post("/auth/users/", data, content_type="application/json")
        # Получение токена
        response = self.client.post("/auth/jwt/create/", data, content_type="application/json")
        self.token = response.data["access"]
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    # получить список всех профилей пользователей во время аутентификации пользователя запроса
    def test_userprofile_list_authenticated(self):
        response = self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # получить список всех профилей пользователей, пока запрос пользователя не прошел проверку подлинности
    def test_userprofile_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # проверьте, чтобы получить данные профиля аутентифицированного пользователя
    def test_userprofile_detail_retrieve(self):
        user_pk = self.user.data['id']
        response = self.client.get(reverse('profile', kwargs={'pk': user_pk}))
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
