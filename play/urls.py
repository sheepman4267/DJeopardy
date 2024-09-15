from django.urls import path
from .views import PlayView, FullAnswerView, buzz_in, correct, incorrect

app_name = 'play'

urlpatterns = [
    path('game/<int:pk>/', PlayView.as_view(), name='game'),
    path('answer/<int:pk>/', FullAnswerView.as_view(), name='fullanswer'),
    path('button/<int:button_id>/', buzz_in, name='buzz_in'),
    path('game/<int:pk>/correct/', correct, name='correct'),
    path('game/<int:pk>/incorrect/', incorrect, name='incorrect')
]