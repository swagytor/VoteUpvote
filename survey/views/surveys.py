from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, decorators, filters, generics, permissions, response

from survey.models import WatchedSurvey, Survey
from survey.paginators import SurveyPaginator
from survey.permissions import IsSurveyOwner
from survey.serializers import SurveySerializer, SurveyListSerializer, SurveyUpdateSerializer
from survey.services import get_like_notification


class SurveyCreateAPIView(generics.CreateAPIView):
    serializer_class = SurveySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()

        user = self.request.user
        if user.is_authenticated:
            instance.author = user

        instance.save()


class SurveyListAPIView(generics.ListAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveyListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = SurveyPaginator
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['likes_count', 'views_count']
    search_fields = ['$title']


class SurveyRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        instance = super().get_object()

        WatchedSurvey.objects.create(user=user, survey=instance)

        instance.views_count += 1
        instance.save()

        return instance


class SurveyUpdateAPIView(generics.UpdateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveyUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsSurveyOwner]


class SurveyDestroyAPIView(generics.DestroyAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveyListSerializer
    permission_classes = [permissions.IsAuthenticated, IsSurveyOwner]


@decorators.api_view(['GET'])
@decorators.permission_classes([permissions.IsAuthenticated])
def like_survey(request, survey_pk):
    user = request.user
    survey = Survey.objects.filter(pk=survey_pk).first()
    message = None

    watched_survey = WatchedSurvey.objects.filter(user=user, survey=survey_pk).first()

    if watched_survey:
        if watched_survey.like_or_dislike == 'like':
            watched_survey.like_or_dislike = None
            survey.likes_count -= 1
            message = f'Вы убрали лайк с опроса "{survey}"'

        elif watched_survey.like_or_dislike in ('dislike', None):
            watched_survey.like_or_dislike = 'like'
            survey.likes_count += 1
            message = f'Вы поставили лайк опросу "{survey}"'

            author = survey.author
            if author is not None and author.email:
                get_like_notification(survey=survey, user_who_liked=user)

        watched_survey.save()
        survey.save()

        return response.Response({"message": message}, status=status.HTTP_200_OK)

    return response.Response({"error": "Вы не можете поставить оценку так как не посмотрели опрос!"},
                             status=status.HTTP_400_BAD_REQUEST)


@decorators.api_view(['GET'])
@decorators.permission_classes([permissions.IsAuthenticated])
def dislike_survey(request, survey_pk):
    user = request.user
    survey = Survey.objects.filter(pk=survey_pk).first()
    message = None

    watched_survey = WatchedSurvey.objects.filter(user=user, survey=survey_pk).first()

    if watched_survey:
        if watched_survey.like_or_dislike == 'dislike':
            watched_survey.like_or_dislike = None
            survey.likes_count += 1
            message = f'Вы убрали дизлайк с опроса "{survey}"'

        elif watched_survey.like_or_dislike in ('like', None):
            watched_survey.like_or_dislike = 'dislike'
            survey.likes_count -= 1
            message = f'Вы поставили дизлайк опросу "{survey}"'

        watched_survey.save()
        survey.save()

        return response.Response({"message": message}, status=status.HTTP_200_OK)

    return response.Response({"error": "Вы не можете поставить оценку так как не посмотрели опрос!"},
                             status=status.HTTP_400_BAD_REQUEST)
