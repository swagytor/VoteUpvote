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
    likes_count = models.PositiveIntegerField(default=0, verbose_name='Количество лайков', blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Автор', **NULLABLE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Question(models.Model):
    ANSWER_CHOICES = (
        ('A', 'Вариант A'),
        ('B', 'Вариант B'),
        ('C', 'Вариант C'),
        ('D', 'Вариант D')
    )

    body = models.CharField(max_length=200, verbose_name='Вопрос')
    answer = models.CharField(max_length=1, choices=ANSWER_CHOICES, default='A', verbose_name='Вариант ответа')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name='Опрос')

    def __str__(self):
        return f"Опрос {self.survey.title} вопрос №{self.pk}"

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
