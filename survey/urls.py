from django.urls import path
from rest_framework.routers import SimpleRouter

from survey.apps import SurveyConfig
from survey.views.questions import QuestionViewSet
from survey.views import surveys

app_name = SurveyConfig.name

survey_router = SimpleRouter()
question_router = SimpleRouter()

survey_router.register('survey', surveys.SurveyViewSet, basename='survey')
question_router.register('question', QuestionViewSet, basename='question')

urlpatterns = [
                  path('survey/<int:pk>/like/', surveys.like_survey, name='survey-like'),
                  path('survey/<int:pk>/dislike/', surveys.dislike_survey, name='survey-dislike'),

                  path('favorites/', surveys.FavoritesSurveyListAPIView.as_view(), name='survey-favorite'),
                  path('my_surveys/', surveys.MySurveyListAPIView.as_view(), name='my-survey'),
                  path('history/', surveys.SurveyHistoryListAPIView.as_view(), name='survey-history'),

              ] + survey_router.urls + question_router.urls
