from django.shortcuts import render

from .models import Game
from .serializers import GameSerializer
from rest_framework import generics

class GameListCreate(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


# Create your views here.
