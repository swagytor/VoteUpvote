from django.urls import path

from users.apps import UsersConfig
from users.views import vk_authentication, FavoritesSurveyListAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('authentication/vk/', vk_authentication, name='auth-vk'),
    path('favorites/', FavoritesSurveyListAPIView.as_view(), name='survey-favorite')
]
