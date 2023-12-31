# Generated by Django 4.2.6 on 2023-10-24 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=200, verbose_name='Вопрос')),
                ('answer', models.CharField(choices=[('A', 'Вариант A'), ('B', 'Вариант B'), ('C', 'Вариант C'), ('D', 'Вариант D')], default='A', max_length=1, verbose_name='Вариант ответа')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.survey', verbose_name='Опрос')),
            ],
        ),
    ]
