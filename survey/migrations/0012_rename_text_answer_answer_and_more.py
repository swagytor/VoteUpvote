# Generated by Django 4.2.6 on 2023-10-26 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0011_alter_watchedsurvey_survey_alter_watchedsurvey_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='text',
            new_name='answer',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='body',
            new_name='question',
        ),
    ]
