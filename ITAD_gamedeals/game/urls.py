from django.urls import path
from . import views

urlpatterns = [
    path('api/game/', views.GameListCreate.as_view()),
]