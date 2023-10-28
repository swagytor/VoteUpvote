from django.conf import settings
from django.core.mail import send_mail

from survey.models import Question, Choice


def get_like_notification(survey, user_who_liked):
    message = (
        f'Пользователь {(user_who_liked.first_name if user_who_liked.first_name else user_who_liked.email)}'
        f'лайкнул ваш опрос "{survey.title}"\n'
        "Самое время гордиться:)")

    author_email = survey.author.email

    send_mail(
        subject='Пользователь лайкнул ваш опрос',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[author_email]
    )


def validate_questions(instance, questions_data):
    for question_data in questions_data:
        question_id = question_data.get('pk', None)
        if question_id:
            question = Question.objects.get(pk=question_data.pk)
            question.question = question_data.get('question', question.question)
            question.answer = question_data.get('answer', question.answer)
            question.save()

            choices = question_data.get('choices', None)

            if choices:
                question.choices.all().delete()

                for option in choices:
                    Choice.objects.create(question=question, **option)
        else:
            validate_new_question(instance, question_data)


def validate_new_question(survey, validated_data):
    choices = None

    if validated_data.get('choices'):
        choices = validated_data.pop('choices')

    question = Question.objects.create(survey=survey, **validated_data)

    if choices is not None:
        for option in choices:
            Choice.objects.create(question=question, **option)

    return question
