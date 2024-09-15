from django.urls import path
from .views import *

app_name = 'host'

urlpatterns = [
    path('', GameListView.as_view(), name='game-list'),
    path('game/<int:pk>/', GameDetailView.as_view(), name='game-detail'),
    path('game/create/', GameCreateView.as_view(), name='game-create'),
    path('category/create/', CategoryCreateView.as_view(), name='category-create'),
    path('answer/create/', AnswerCreateView.as_view(), name='answer-create'),
    path('player/create/', PlayerCreateView.as_view(), name='player-create'),
]