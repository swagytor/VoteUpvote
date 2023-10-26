from django.db import models

from users.models import User

NULLABLE = {
    'blank': True,
    'null': True
}


# Create your models here.
class Survey(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    likes_count = models.IntegerField(default=0, verbose_name='Количество лайков', blank=True)
    views_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров', blank=True)
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Время публикации', **NULLABLE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Автор', **NULLABLE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Question(models.Model):
    body = models.CharField(max_length=200, verbose_name='Вопрос')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name='Опрос', related_name='questions')

    def __str__(self):
        return f"Опрос {self.survey.title} вопрос №{self.pk}"

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос', related_name='answers')
    text = models.CharField(max_length=100, verbose_name='Ответ')

    def __str__(self):
        return f"{self.text}"

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class WatchedSurvey(models.Model):
    LIKE_OR_DISLIKE_CHOICES = [
        ('LIKE', 'like'),
        ('DISLIKE', 'dislike')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='users')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name='Опрос', related_name='surveys')
    like_or_dislike = models.CharField(max_length=7, choices=LIKE_OR_DISLIKE_CHOICES, default=None,
                                       verbose_name='Оценка', **NULLABLE)

    def __str__(self):
        return f"Пользователь:{self.user.username} Опрос:{self.survey.title}"

    class Meta:
        verbose_name = 'Просмотренный опрос'
        verbose_name_plural = 'Просмотренные опросы'
