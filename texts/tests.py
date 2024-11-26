from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Text
from persons.models import Person
from rest_framework_simplejwt.tokens import RefreshToken
# Create your tests here.


class UrlTest(APITestCase):

    def setUp(self):
        self.person_one = Person.objects.create(
            username='test', password='test1234')
        self.person_two = Person.objects.create(
            username='test2', password='test1234')

    def __jwt_auth(self, user):
        refresh_token = RefreshToken().for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(refresh_token.access_token))

    def test_person_can_see_received_texts_list(self):
        self.__jwt_auth(self.person_one)
        r_received_texts = self.client.get(
            f"/api/v1/texts/received/list/{self.person_two.id}/")
        self.assertEqual(r_received_texts.status_code, 200)

    def test_person_can_see_sent_texts_list(self):
        self.__jwt_auth(self.person_one)
        r_sent_texts = self.client.get(
            f"/api/v1/texts/sent/list/{self.person_two.id}/")
        self.assertEqual(r_sent_texts.status_code, 200)

    def test_person_can_send_text(self):
        self.__jwt_auth(self.person_one)
        r_sent_text = self.client.post(
            f"/api/v1/texts/send/{self.person_two.id}/", {"content": "hello baby."})
        self.assertEqual(r_sent_text.status_code, 200)

    def test_person_can_edit_text(self):
        self.__jwt_auth(self.person_one)
        text = Text.objects.create(
            content="test1", sender=self.person_one, recipient=self.person_two)
        r_edit_text = self.client.patch(
            f"/api/v1/texts/edit/{text.id}/")
        self.assertEqual(r_edit_text.status_code, 200)

    def test_person_cant_edit_other_person_text(self):
        self.__jwt_auth(self.person_two)
        text = Text.objects.create(
            content="test1", sender=self.person_one, recipient=self.person_two)
        r_edit_text = self.client.patch(
            f"/api/v1/texts/edit/{text.id}/")
        self.assertEqual(r_edit_text.status_code, 404)

    def test_person_can_remove_text(self):
        self.__jwt_auth(self.person_one)
        text = Text.objects.create(
            content="test1", sender=self.person_one, recipient=self.person_two)
        r_remove_text = self.client.delete(
            f"/api/v1/texts/remove/{text.id}/")
        self.assertEqual(r_remove_text.status_code, 204)

    def test_person_cant_edit_other_person_text(self):
        self.__jwt_auth(self.person_two)
        text = Text.objects.create(
            content="test1", sender=self.person_one, recipient=self.person_two)
        r_remove_text = self.client.delete(
            f"/api/v1/texts/remove/{text.id}/")
        self.assertEqual(r_remove_text.status_code, 404)
