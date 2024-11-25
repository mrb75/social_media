from rest_framework import serializers
from .models import *


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ["person"]

    def create(self, validated_data):
        post = Post(**validated_data)
        post.person = self.context['request'].user
        post.save()
        return post


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        exclude = ["post"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ["post"]
