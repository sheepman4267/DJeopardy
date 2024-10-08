import django_eventstream
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, UpdateView
from host.models import Game, Answer, Player


# Create your views here.


class PlayView(DetailView):
    model = Game
    template_name = 'play/play_board.html'
    context_object_name = 'game'
    extra_context = {
        'answer_template': 'play/answer.html'
    }

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        categories = context['game'].categories.all()
        paginator = Paginator(categories, context['game'].page_size)
        context['page'] = paginator.page(self.request.GET.get('page'))
        context['page_number'] = self.request.GET.get('page')
        context['next_page'] = int(self.request.GET.get('page')) + 1
        context['previous_page'] = int(self.request.GET.get('page')) - 1
        return context


class FullAnswerView(DetailView):
    model = Answer
    template_name = 'play/answer_full.html'

    def get_object(self, queryset=None):
        answer = super(self.__class__, self).get_object(queryset)
        answer.category.game.current_answer = answer
        answer.category.game.save()
        return answer


def buzz_in(request, button_id):
    player = get_object_or_404(Player, button_id=button_id)
    if player.game.current_answer and not player.game.current_player:
        player.game.current_player = player
        player.game.save()
    else:
        print(f'Not buzzing in {player}. Current Answer: {player.game.current_answer}. Current Player: {player.game.current_player}')
    django_eventstream.send_event("test", "message", player.name)
    return HttpResponse(f'OK {player}')


def correct(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    game = answer.category.game
    player = game.current_player
    player.points += game.current_answer.points
    player.save()
    game.current_answer = None
    game.current_player = None
    game.save()
    answer.completed = True
    answer.save()
    return render(
        request,
        'play/correct.html',
        context={
            'player': player,
            'game': game,
            'answer': answer,
        }
    )


def incorrect(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    game = answer.category.game
    player = game.current_player
    player.points -= game.current_answer.points
    player.save()
    game.current_player = None
    game.save()
    return render(
        request,
        'play/incorrect.html',
        context={
            'player': player,
            'game': game,
            'answer': answer,
        }
    )


