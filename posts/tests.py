from django.test import TestCase
from rest_framework.test import APITestCase
from .models import *
from persons.models import Person
from rest_framework_simplejwt.tokens import RefreshToken
import environ


# Create your tests here.


class UrlTest(APITestCase):

    def setUp(self):
        self.person_one = Person.objects.create(
            username='test', password='test1234')
        self.person_two = Person.objects.create(
            username='test2', password='test1234')
        self.env = environ.Env(
            # set casting, default value
            DEBUG=(bool, False)
        )

    def __jwt_auth(self, user):
        refresh_token = RefreshToken().for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(refresh_token.access_token))

    def test_person_can_add_post(self):
        self.__jwt_auth(self.person_one)
        r_add_post = self.client.post("/api/v1/posts/personal/")
        self.assertEqual(r_add_post.status_code, 201)

    def test_person_can_see_personal_posts_list(self):
        self.__jwt_auth(self.person_one)
        r_post_list = self.client.get("/api/v1/posts/personal/")
        self.assertEqual(r_post_list.status_code, 200)

    def test_person_can_see_post_detail(self):
        self.__jwt_auth(self.person_one)
        post = Post.objects.create(
            person=self.person_one, caption="test is test")
        r_post_detail = self.client.get(f"/api/v1/posts/personal/{post.id}/")
        self.assertEqual(r_post_detail.status_code, 200)

    def test_person_cant_see_other_person_post_detail(self):
        self.__jwt_auth(self.person_one)
        post = Post.objects.create(
            person=self.person_two, caption="test is test")
        r_post_detail = self.client.get(f"/api/v1/posts/personal/{post.id}/")
        self.assertEqual(r_post_detail.status_code, 404)

    def test_person_can_edit_post_detail(self):
        self.__jwt_auth(self.person_one)
        post = Post.objects.create(
            person=self.person_one, caption="test is test")
        r_post_edit = self.client.get(f"/api/v1/posts/personal/{post.id}/")
        self.assertEqual(r_post_edit.status_code, 200)

    def test_person_cant_edit_other_person_post_detail(self):
        self.__jwt_auth(self.person_one)
        post = Post.objects.create(
            person=self.person_two, caption="test is test")
        r_post_edit = self.client.get(f"/api/v1/posts/personal/{post.id}/")
        self.assertEqual(r_post_edit.status_code, 404)

    def test_person_can_remove_post(self):
        self.__jwt_auth(self.person_one)
        post = Post.objects.create(
            person=self.person_one, caption="test is test")
        r_post_remove = self.client.delete(
            f"/api/v1/posts/personal/{post.id}/")
        self.assertEqual(r_post_remove.status_code, 204)

    def test_person_cant_remove_other_person_post(self):
        self.__jwt_auth(self.person_one)
        post = Post.objects.create(
            person=self.person_two, caption="test is test")
        r_post_remove = self.client.delete(
            f"/api/v1/posts/personal/{post.id}/")
        self.assertEqual(r_post_remove.status_code, 404)

    # def test_can_add_image_to_post(self):
    #     self.__jwt_auth(self.person_one)
    #     post = Post.objects.create(
    #         person=self.person_two, caption="test is test")
    #     data = {"path": self.env("TEST_IMAGE_LOCATION")}
    #     r_post_add_image = self.client.post(
    #         f"/api/v1/posts/images/add/{post.id}/", data=data, format="multipart")
    #     self.assertEqual(r_post_add_image.status_code, 200)

    def test_person_can_see_post_comments(self):
        self.__jwt_auth(self.person_one)
        post = Post.objects.create(
            person=self.person_two, caption="test is test")
        r_post_comments = self.client.get(f"/api/v1/posts/comments/{post.id}/")
        self.assertEqual(r_post_comments.status_code, 200)

    def test_person_can_add_comment_to_post(self):
        self.__jwt_auth(self.person_one)
        post = Post.objects.create(
            person=self.person_two, caption="test is test")
        r_add_comment = self.client.post(
            f"/api/v1/posts/comments/add/{post.id}/", {"text": "texty text"})
        self.assertEqual(r_add_comment.status_code, 200)

    def test_person_can_see_comment_detail(self):
        self.__jwt_auth(self.person_one)
        post = Post.objects.create(
            person=self.person_one, caption="test is test")
        comment = post.comments.create(text="texty text", post=post)
        r_post_comment = self.client.get(
            f"/api/v1/posts/comments/detail/{comment.id}/")
        self.assertEqual(r_post_comment.status_code, 200)

    def test_person_cant_see_other_person_comment_detail(self):
        self.__jwt_auth(self.person_one)
        post = Post.objects.create(
            person=self.person_two, caption="test is test")
        comment = post.comments.create(text="texty text", post=post)
        r_post_comment = self.client.get(
            f"/api/v1/posts/comments/detail/{comment.id}/")
        self.assertEqual(r_post_comment.status_code, 404)

    def test_person_can_edit_comment_detail(self):
        self.__jwt_auth(self.person_one)
        post = Post.objects.create(
            person=self.person_one, caption="test is test")
        comment = post.comments.create(text="texty text", post=post)
        r_post_comment_edit = self.client.patch(
            f"/api/v1/posts/comments/edit/{comment.id}/", {"text": "texty text 2"})
        self.assertEqual(r_post_comment_edit.status_code, 200)

    def test_person_cant_edit_other_person_comment_detail(self):
        self.__jwt_auth(self.person_one)
        post = Post.objects.create(
            person=self.person_two, caption="test is test")
        comment = post.comments.create(text="texty text", post=post)
        r_post_comment_edit = self.client.patch(
            f"/api/v1/posts/comments/edit/{comment.id}/", {"text": "texty text 2"})
        self.assertEqual(r_post_comment_edit.status_code, 404)

    def test_person_can_remove_comment_detail(self):
        self.__jwt_auth(self.person_one)
        post = Post.objects.create(
            person=self.person_one, caption="test is test")
        comment = post.comments.create(text="texty text", post=post)
        r_post_comment_remove = self.client.delete(
            f"/api/v1/posts/comments/remove/{comment.id}/", {"text": "texty text 2"})
        self.assertEqual(r_post_comment_remove.status_code, 204)

    def test_person_cant_remove_other_person_comment_detail(self):
        self.__jwt_auth(self.person_one)
        post = Post.objects.create(
            person=self.person_two, caption="test is test")
        comment = post.comments.create(text="texty text", post=post)
        r_post_comment_remove = self.client.delete(
            f"/api/v1/posts/comments/remove/{comment.id}/")
        self.assertEqual(r_post_comment_remove.status_code, 404)
