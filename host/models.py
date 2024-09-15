from django.db import models
from django.urls import reverse_lazy


class Game(models.Model):
    name = models.CharField(max_length=100)
    current_answer = models.ForeignKey('Answer', on_delete=models.CASCADE, null=True, blank=True)
    current_player = models.ForeignKey('Player', on_delete=models.CASCADE, null=True, blank=True, related_name='+')

    def __str__(self):
        return self.name

    def get_max_questions(self):
        # this is for dynamically setting the correct number of grid rows in CSS
        category_question_numbers = []
        for category in self.categories.all():
            category_question_numbers.append(category.questions.count())
        return max(category_question_numbers)

    def get_absolute_url(self):
        return reverse_lazy('host:game-detail', kwargs={'pk': self.pk})


class Category(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name


class Answer(models.Model):
    answer = models.TextField()
    points = models.IntegerField()
    completed = models.BooleanField(default=False)
    double = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='answers')
    question = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.answer

    class Meta:
        ordering = ['points',]


class Player(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='players')
    name = models.CharField(max_length=100)
    points = models.IntegerField(default=0)
    button_id = models.IntegerField(default=0)

    def __str__(self):
        return self.name
