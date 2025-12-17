from rest_framework import generics # Generic - це готові класи представлень, які надають базову функціональність для створення API.
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]  # Дозволяє доступ до цього представлення будь-кому, навіть неавторизованим користувачам.
    serializer_class = UserRegistrationSerializer