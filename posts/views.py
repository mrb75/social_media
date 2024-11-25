from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import *
from .filters import *
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, RetrieveAPIView, UpdateAPIView
from .models import *
from rest_framework.response import Response


class PostsViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    filterset_class = PostFilterSet

    def get_queryset(self):
        return self.request.user.posts.all()


class PostImageView(ListAPIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostImageSerializer

    def get_queryset(self):
        post_id = None
        if 'pk' in self.kwargs and isinstance(self.kwargs['pk'], int):
            post_id = self.kwargs["pk"]
        return get_object_or_404(Post, pk=post_id).images.all()


class AddPostImageView(CreateAPIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostImageSerializer

    def get_queryset(self):
        post_id = None
        if 'pk' in self.kwargs and isinstance(self.kwargs['pk'], int):
            post_id = self.kwargs["pk"]
        return get_object_or_404(Post, pk=post_id).images.all()

    def create(self, request, *args, **kwargs):
        post_id = self.kwargs["pk"]
        image_serializer = PostImageSerializer(data=request.data)
        if (image_serializer.is_valid()):
            post = get_object_or_404(
                Post, pk=post_id).images.create(**image_serializer.validated_data)

            return Response(status=200)
        else:
            return Response(image_serializer.errors, 400)


class RemovePostImageView(DestroyAPIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostImageSerializer

    def get_queryset(self):
        return PostImage.objects.filter(post__person=self.request.user)


class CommentListView(ListAPIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = None
        if 'pk' in self.kwargs and isinstance(self.kwargs['pk'], int):
            post_id = self.kwargs["pk"]
        return get_object_or_404(Post, pk=post_id).comments.all()


class AddCommentView(CreateAPIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = None
        if 'pk' in self.kwargs and isinstance(self.kwargs['pk'], int):
            post_id = self.kwargs["pk"]
        return get_object_or_404(Post, pk=post_id).comments.all()

    def create(self, request, *args, **kwargs):
        post_id = self.kwargs["pk"]
        comment_serializer = CommentSerializer(data=request.data)
        if (comment_serializer.is_valid()):
            post = get_object_or_404(
                Post, pk=post_id).comments.create(**comment_serializer.validated_data)

            return Response(status=200)
        else:
            return Response(image_serializer.errors, 400)


class CommentDetailView(RetrieveAPIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post__person=self.request.user)


class EditCommentView(UpdateAPIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post__person=self.request.user)


class RemoveCommentView(DestroyAPIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post__person=self.request.user)
