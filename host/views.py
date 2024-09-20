from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Game, Category, Answer, Player
from django_eventstream import send_event


class GameListView(ListView):
    model = Game
    context_object_name = 'games'
    template_name = 'host/game_list.html'
    def get_context_data(self, **kwargs):
        # send_event(<channel>, <event_type>, <event_data>)
        send_event("test", "message", "hello world")
        print('ping')
        return super(self.__class__, self).get_context_data(**kwargs)


class GameCreateView(CreateView):
    model = Game
    template_name = 'host/game_create.html'
    fields = [
        "name",
    ]


class GameUpdateView(UpdateView):
    model = Game
    fields = [
        "name",
        "page_size"
    ]
    template_name = 'host/game_update.html'


class GameDetailView(DetailView):
    model = Game
    context_object_name = 'game'
    template_name = 'host/edit.html'
    extra_context = {
        'answer_template': 'host/answer.html',
        'host': True,
    }


class CategoryCreateView(CreateView):
    model = Category
    fields = [
        "name",
        "game",
    ]
    template_name = 'host/category_create.html'
    def get_success_url(self):
        return reverse_lazy('host:game-detail', kwargs={'pk': self.object.game.pk})


class AnswerCreateView(CreateView):
    model = Answer
    fields = [
        "answer",
        "points",
        "double",
        "category",
        "question",
    ]
    template_name = 'host/answer_create.html'

    def get_success_url(self):
        return reverse_lazy('host:game-detail', kwargs={'pk': self.object.category.game.pk})


class AnswerUpdateView(UpdateView):
    model = Answer
    fields = [
        "answer",
        "points",
        "double",
        "question",
        "completed",
    ]
    template_name = 'host/answer_update.html'

    def get_success_url(self):
        return reverse_lazy('host:game-detail', kwargs={'pk': self.object.category.game.pk})


class PlayerCreateView(CreateView):
    model = Player
    fields = [
        "name",
        "game",
        "button_id",
    ]
    template_name = 'host/player_create.html'

    def get_success_url(self):
        return reverse_lazy('host:game-detail', kwargs={'pk': self.object.game.pk})


class PLayerUpdateView(UpdateView):
    model = Player
    fields = [
        "name",
        "button_id",
    ]
    template_name = 'host/player_update.html'

    def get_success_url(self):
        return reverse_lazy('host:game-detail', kwargs={'pk': self.object.game.pk})
