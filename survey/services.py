from django.conf import settings
from django.core.mail import send_mail


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
