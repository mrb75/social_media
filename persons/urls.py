from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()


urlpatterns = [
    path("register", RegisterView.as_view()),
    path("changePassword", ChangePasswordView.as_view()),
]

urlpatterns += router.urls
