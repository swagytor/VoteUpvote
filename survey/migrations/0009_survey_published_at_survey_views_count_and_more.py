# Generated by Django 4.2.6 on 2023-10-25 22:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0008_alter_question_options_alter_usersurvey_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='published_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Время публикации'),
        ),
        migrations.AddField(
            model_name='survey',
            name='views_count',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='Количество просмотров'),
        ),
        migrations.AlterField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='survey.survey', verbose_name='Опрос'),
        ),
    ]
