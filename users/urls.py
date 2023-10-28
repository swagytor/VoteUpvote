from django.urls import path

from users.apps import UsersConfig
from users.views import vk_authentication, FavoritesSurveyListAPIView, MySurveyListAPIView, SurveyHistoryListAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('authentication/vk/', vk_authentication, name='auth-vk'),
    path('favorites/', FavoritesSurveyListAPIView.as_view(), name='survey-favorite'),
    path('my_surveys/', MySurveyListAPIView.as_view(), name='survey-user'),
    path('history/', SurveyHistoryListAPIView.as_view(), name='survey-history')
]
