from django.shortcuts import render
from .models import Text
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import TextSerializer
from django.shortcuts import get_object_or_404
from persons.models import Person
from rest_framework.response import Response
# Create your views here.


class ReceivedTextsView(ListAPIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TextSerializer

    def get_queryset(self):
        sender_id = None
        if 'pk' in self.kwargs and isinstance(self.kwargs['pk'], int):
            sender_id = self.kwargs["pk"]

        sender = get_object_or_404(Person, pk=sender_id)
        return self.request.user.receivedTexts.filter(sender=sender)


class SentTextsView(ListAPIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TextSerializer

    def get_queryset(self):
        recipient_id = None
        if 'pk' in self.kwargs and isinstance(self.kwargs['pk'], int):
            recipient_id = self.kwargs["pk"]

        recipient = get_object_or_404(Person, pk=recipient_id)
        return self.request.user.sentTexts.filter(recipient=recipient)


class SendTextView(CreateAPIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TextSerializer

    def get_queryset(self):
        recipient_id = None
        if 'pk' in self.kwargs and isinstance(self.kwargs['pk'], int):
            recipient_id = self.kwargs["pk"]

        recipient = get_object_or_404(Person, pk=recipient_id)
        return self.request.user.sentTexts.filter(recipient=recipient)

    def create(self, request, *args, **kwargs):
        recipient_id = None
        if 'pk' in self.kwargs and isinstance(self.kwargs['pk'], int):
            recipient_id = self.kwargs["pk"]

        recipient = get_object_or_404(Person, pk=recipient_id)
        text_serializer = TextSerializer(data=request.data)
        if text_serializer.is_valid():
            text_serializer.create(
                text_serializer.validated_data, recipient, request.user)
            return Response(status=200)
        else:
            return Response(image_serializer.errors, 400)


class EditTextView(UpdateAPIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TextSerializer

    def get_queryset(self):
        return self.request.user.sentTexts.all()


class RemoveTextView(DestroyAPIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TextSerializer

    def get_queryset(self):
        return self.request.user.sentTexts.all()
