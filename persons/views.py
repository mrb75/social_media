from django.shortcuts import render
from rest_framework.views import APIView
from socialMedia.permissions import IsNotAuthenticated
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import Person
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.


class RegisterView(APIView):
    permission_classes = [IsNotAuthenticated]

    def post(self, request):
        register_serializer = RegisterSerializer(data=request.data)
        if (register_serializer.is_valid()):
            person_data = register_serializer.data
            person_data.pop("password_confirmation")
            password = person_data.pop("password")
            person = Person(**person_data)
            person.set_password(password)
            person.save()
            return Response(status=200)
        else:
            return Response(register_serializer.errors, 400)


class ChangePasswordView(APIView):
    authentication_classes = [TokenAuthentication,
                              JWTAuthentication]
    permission_classes = [
        IsAuthenticated
    ]

    def patch(self, request):
        person = request.user
        person_serializer = ChangePasswordSerializer(data=request.data)
        if person_serializer.is_valid():
            old_password = person_serializer.data.pop("old_password")
            person_serializer.data.pop("old_password")
            if old_password == person.password:
                password = person_serializer.data.pop("password")
                person.set_password(password)
                person.save()
                return Response(status=204)
            else:
                return Response("password is not correct", 400)
        else:
            return Response(person_serializer.errors, 400)
