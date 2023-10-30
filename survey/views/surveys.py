from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, decorators, filters, permissions, response, viewsets, generics

from survey.models import WatchedSurvey, Survey
from survey.permissions import IsSurveyOwner
from survey import serializers
from survey.services import get_like_notification


class MultiSerializerViewSet(viewsets.ModelViewSet):
    serializers = {
        'default': None,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action,
                                    self.serializers['default'])


class SurveyViewSet(MultiSerializerViewSet):
    queryset = Survey.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsSurveyOwner]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['likes_count', 'views_count']
    search_fields = ['$title', '$description']

    serializers = {
        'create': serializers.SurveyQuestionSerializer,
        'list': serializers.SurveySerializer,
        'retrieve': serializers.SurveyQuestionSerializer,
        'update': serializers.SurveyUpdateSerializer,
        'default': serializers.SurveySerializer,
    }

    def perform_create(self, serializer):
        """Метод для автоматического определения автора у объекта Survey"""
        instance = serializer.save()

        user = self.request.user
        if user.is_authenticated:
            instance.author = user

        instance.save()

    def get_object(self):
        """Метод для создания объекта WatchedSurvey при прочтении объекта Survey"""
        user = self.request.user
        instance = super().get_object()

        if self.action == 'retrieve':

            watched_survey = WatchedSurvey.objects.filter(user=user, survey=instance)

            if not watched_survey.exists():
                WatchedSurvey.objects.create(user=user, survey=instance)

            instance.views_count += 1
            instance.save()

        return instance


@decorators.api_view(['GET'])
@decorators.permission_classes([permissions.IsAuthenticated])
def like_survey(request, pk):
    """Контроллер для добавления лайка к опросу"""
    user = request.user
    survey = Survey.objects.filter(pk=pk).first()
    message = None

    # ищем опрос среди просмотренных пользователем опросов
    watched_survey = WatchedSurvey.objects.filter(user=user, survey=pk).first()

    # если находим, то ставим лайк
    if watched_survey:
        # если лайк уже стоит, то мы его убираем
        if watched_survey.like_or_dislike == 'like':
            watched_survey.like_or_dislike = None
            survey.likes_count -= 1
            message = f'Вы убрали лайк с опроса "{survey}"'

        # если лайк не стоит, то мы его ставим
        elif watched_survey.like_or_dislike in ('dislike', None):
            watched_survey.like_or_dislike = 'like'
            survey.likes_count += 1
            message = f'Вы поставили лайк опросу "{survey}"'

            author = survey.author
            # если у автора опроса будет указана почта, то мы отправим ему уведомление по почте
            if author is not None and author.email:
                get_like_notification(survey=survey, user_who_liked=user)

        watched_survey.save()
        survey.save()

        return response.Response({"message": message}, status=status.HTTP_200_OK)

    # если не нашёлся просмотренный опрос, выводим ошибку
    return response.Response({"error": "Вы не можете поставить оценку так как не посмотрели опрос!"},
                             status=status.HTTP_400_BAD_REQUEST)


@decorators.api_view(['GET'])
@decorators.permission_classes([permissions.IsAuthenticated])
def dislike_survey(request, pk):
    """Контроллер для добавления дизлайка к опросу"""
    user = request.user
    survey = Survey.objects.filter(pk=pk).first()
    message = None
    # ищем опрос среди просмотренных пользователем опросов
    watched_survey = WatchedSurvey.objects.filter(user=user, survey=pk).first()

    # если находим, то ставим дизлайк
    if watched_survey:

        # если дизлайк уже стоит, то мы его убираем
        if watched_survey.like_or_dislike == 'dislike':
            watched_survey.like_or_dislike = None
            survey.likes_count += 1
            message = f'Вы убрали дизлайк с опроса "{survey}"'

        # если дизлайк не стоит, то мы его ставим
        elif watched_survey.like_or_dislike in ('like', None):
            watched_survey.like_or_dislike = 'dislike'
            survey.likes_count -= 1
            message = f'Вы поставили дизлайк опросу "{survey}"'

        watched_survey.save()
        survey.save()

        return response.Response({"message": message}, status=status.HTTP_200_OK)
    # если не нашёлся просмотренный опрос, выводим ошибку
    return response.Response({"error": "Вы не можете поставить оценку так как не посмотрели опрос!"},
                             status=status.HTTP_400_BAD_REQUEST)


class FavoritesSurveyListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.FavoriteSerializer
    queryset = WatchedSurvey.objects.all()

    def get_queryset(self):
        user = self.request.user

        queryset = super().get_queryset()

        queryset = queryset.filter(user=user, like_or_dislike='like')

        return queryset


class MySurveyListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.SurveySerializer
    queryset = Survey.objects.all()

    def get_queryset(self):
        user = self.request.user

        queryset = super().get_queryset()

        queryset = queryset.filter(author=user)

        return queryset


class SurveyHistoryListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.FavoriteSerializer
    queryset = WatchedSurvey.objects.all()

    def get_queryset(self):
        user = self.request.user

        queryset = super().get_queryset()

        queryset = queryset.filter(user=user)

        return queryset

# class SurveyCreateAPIView(generics.CreateAPIView):
#     """Контроллер для создания объекта Survey"""
#     serializer_class = SurveyQuestionSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def perform_create(self, serializer):
#         """Метод для автоматического определения автора у объекта Survey"""
#         instance = serializer.save()
#
#         user = self.request.user
#         if user.is_authenticated:
#             instance.author = user
#
#         instance.save()
#
#
# class SurveyListAPIView(generics.ListAPIView):
#     """Контроллер для получения списка объектов Survey"""
#     queryset = Survey.objects.all()
#     serializer_class = SurveySerializer
#     permission_classes = [permissions.IsAuthenticated]
#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
#     ordering_fields = ['likes_count', 'views_count']
#     search_fields = ['$title', '$description']
#
#
# class SurveyRetrieveAPIView(generics.RetrieveAPIView):
#     """Контроллер для получения детальной информации объекта Survey"""
#     queryset = Survey.objects.all()
#     serializer_class = SurveyQuestionSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_object(self):
#         """Метод для создания объекта WatchedSurvey при прочтении объекта Survey"""
#         user = self.request.user
#         instance = super().get_object()
#
#         watched_survey = WatchedSurvey.objects.filter(user=user, survey=instance)
#
#         if not watched_survey.exists():
#             WatchedSurvey.objects.create(user=user, survey=instance)
#
#         instance.views_count += 1
#         instance.save()
#
#         return instance
#
#
# class SurveyUpdateAPIView(generics.UpdateAPIView):
#     """Контроллер для обновления объекта Survey"""
#     queryset = Survey.objects.all()
#     serializer_class = SurveyUpdateSerializer
#     permission_classes = [permissions.IsAuthenticated, IsSurveyOwner]
#
#
# class SurveyDestroyAPIView(generics.DestroyAPIView):
#     """Контроллер для удаления объекта Survey"""
#     queryset = Survey.objects.all()
#     permission_classes = [permissions.IsAuthenticated, IsSurveyOwner]
