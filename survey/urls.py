from django.urls import path

from survey.apps import SurveyConfig
from survey.views.questions import QuestionCreateAPIView, QuestionUpdateAPIView, QuestionListAPIView, \
    QuestionRetrieveAPIView, QuestionDestroyAPIView
from survey.views.surveys import SurveyCreateAPIView, SurveyListAPIView, SurveyRetrieveAPIView, SurveyUpdateAPIView, \
    SurveyDestroyAPIView, like_survey, dislike_survey

app_name = SurveyConfig.name


urlpatterns = [
    path('survey/create/', SurveyCreateAPIView.as_view(), name='survey-create'),
    path('', SurveyListAPIView.as_view(), name='survey-list'),
    path('survey/<int:pk>/', SurveyRetrieveAPIView.as_view(), name='survey-get'),
    path('survey/<int:pk>/update/', SurveyUpdateAPIView.as_view(), name='survey-update'),
    path('survey/<int:pk>/delete/', SurveyDestroyAPIView.as_view(), name='survey-delete'),

    path('survey/<int:pk>/like/', like_survey, name='survey-like'),
    path('survey/<int:pk>/dislike/', dislike_survey, name='survey-dislike'),

    path('question/create/', QuestionCreateAPIView.as_view(), name='question-create'),
    path('questions/', QuestionListAPIView.as_view(), name='question-list'),
    path('question/<int:pk>/', QuestionRetrieveAPIView.as_view(), name='question-get'),
    path('question/<int:pk>/update/', QuestionUpdateAPIView.as_view(), name='question-update'),
    path('question/<int:pk>/delete/', QuestionDestroyAPIView.as_view(), name='question-delete'),

]
