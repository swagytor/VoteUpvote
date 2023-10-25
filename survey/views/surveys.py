from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from survey.models import UserSurvey, Survey
from survey.paginators import SurveyPaginator
from survey.serializers import SurveySerializer, SurveyListSerializer, SurveyUpdateSerializer


class SurveyCreateAPIView(CreateAPIView):
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()

        user = self.request.user
        if user.is_authenticated:
            instance.author = user

        instance.save()


class SurveyListAPIView(ListAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveyListSerializer
    permission_classes = [IsAuthenticated]


class SurveyRetrieveAPIView(RetrieveAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        instance = super().get_object()

        UserSurvey.objects.create(user=user, survey=instance)

        instance.views_count += 1
        instance.save()

        return instance


class SurveyUpdateAPIView(UpdateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveyUpdateSerializer
    permission_classes = [IsAuthenticated]


class SurveyDestroyAPIView(DestroyAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveyListSerializer
    permission_classes = [IsAuthenticated]
