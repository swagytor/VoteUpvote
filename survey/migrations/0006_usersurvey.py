# Generated by Django 4.2.6 on 2023-10-25 08:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0005_remove_answer_user_alter_answer_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSurvey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.survey', verbose_name='Опрос')),
            ],
        ),
    ]