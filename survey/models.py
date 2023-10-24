from django.db import models

NULLABLE = {
    'blank': True,
    'null': True
}


# Create your models here.
# class Survey(models.Model):
#     title = models.CharField(max_length=100, verbose_name='Название')
#     description = models.TextField(verbose_name='Описание')
#     likes_count = models.PositiveIntegerField(default=0, verbose_name='Количество лайков', blank=True)
#     author = models.ForeignKey(User)
