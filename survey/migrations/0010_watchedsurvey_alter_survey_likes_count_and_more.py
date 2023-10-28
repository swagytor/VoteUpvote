# Generated by Django 4.2.6 on 2023-10-26 00:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('survey', '0009_survey_published_at_survey_views_count_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WatchedSurvey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_or_dislike', models.CharField(blank=True, choices=[('LIKE', 'like'), ('DISLIKE', 'dislike')], default=None, max_length=7, null=True, verbose_name='Оценка')),
            ],
            options={
                'verbose_name': 'Просмотренный опрос',
                'verbose_name_plural': 'Просмотренные опросы',
            },
        ),
        migrations.AlterField(
            model_name='survey',
            name='likes_count',
            field=models.IntegerField(blank=True, default=0, verbose_name='Количество лайков'),
        ),
        migrations.DeleteModel(
            name='UserSurvey',
        ),
        migrations.AddField(
            model_name='watchedsurvey',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.survey', verbose_name='Опрос'),
        ),
        migrations.AddField(
            model_name='watchedsurvey',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]