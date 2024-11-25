from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()

router.register(r"personal", PostsViewSet, basename="personalPosts")
urlpatterns = [
    path("images/<int:pk>/", PostImageView.as_view(), name=""),
    path("images/add/<int:pk>/", AddPostImageView.as_view(), name=""),
    path("images/remove/<int:pk>/", RemovePostImageView.as_view(), name=""),
    path("comments/<int:pk>/", CommentListView.as_view(), name=""),
    path("comments/add/<int:pk>/", AddCommentView.as_view(), name=""),
    path("comments/detail/<int:pk>/", CommentDetailView.as_view(), name=""),
    path("comments/edit/<int:pk>/", EditCommentView.as_view(), name=""),
    path("comments/remove/<int:pk>/", RemoveCommentView.as_view(), name=""),
]

urlpatterns += router.urls
