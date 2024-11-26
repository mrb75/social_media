from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Person
from django.contrib.auth.models import Group, Permission
from rest_framework_simplejwt.tokens import RefreshToken
import datetime
from .models import Person
# Create your tests here.


class UrlTest(APITestCase):

    def setUp(self):
        self.person = Person.objects.create(
            username='test', password='test1234')

    def __jwt_auth(self, user):
        refresh_token = RefreshToken().for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(refresh_token.access_token))

    def test_person_can_register(self):
        r_register = self.client.post('/api/v1/persons/register', data={
                                      "username": "test2",
                                      "email": "test@test.test",
                                      "password": "test1234",
                                      "password_confirmation": "test1234"})
        self.assertEqual(r_register.status_code, 200)

    def test_person_cant_register_without_confirmation(self):
        r_register = self.client.post('/api/v1/persons/register', data={
                                      "username": "test2",
                                      "email": "test@test.test",
                                      "password": "test1234",
                                      "password_confirmation": "test123"})
        self.assertEqual(r_register.status_code, 400)

    def test_person_can_change_password(self):
        self.__jwt_auth(self.person)
        r_change_pass = self.client.patch("/api/v1/persons/changePassword", data={"old_password": "test1234",
                                                                                  "password": "test12345",
                                                                                  "password_confirmation": "test12345"})
        self.assertEqual(r_change_pass.status_code, 204)

    def test_person_cant_change_password_without_confirmation(self):
        self.__jwt_auth(self.person)
        r_change_pass = self.client.patch("/api/v1/persons/changePassword", data={"old_password": "test1234",
                                                                                  "password": "test12345",
                                                                                  "password_confirmation": "test1235"})
        self.assertEqual(r_change_pass.status_code, 400)

    def test_person_cant_change_password_without_old_password(self):
        self.__jwt_auth(self.person)
        r_change_pass = self.client.patch("/api/v1/persons/changePassword", data={"old_password": "test123",
                                                                                  "password": "test12345",
                                                                                  "password_confirmation": "test12345"})
        self.assertEqual(r_change_pass.status_code, 400)
