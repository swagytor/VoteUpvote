from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from survey.models import Question
from survey.permissions import IsQuestionOwner
from survey.serializers import QuestionSerializer, CreateQuestionSerializer


class QuestionCreateAPIView(CreateAPIView):
    """Контроллер для создания объекта Question"""
    permission_classes = [IsAuthenticated]
    serializer_class = CreateQuestionSerializer


class QuestionListAPIView(ListAPIView):
    """Контроллер для получения списка объектов Question"""
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class QuestionRetrieveAPIView(RetrieveAPIView):
    """Контроллер для получения детальной информации объекта Question"""
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class QuestionUpdateAPIView(UpdateAPIView):
    """Контроллер для обновления объекта Question"""
    permission_classes = [IsAuthenticated, IsQuestionOwner]
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class QuestionDestroyAPIView(DestroyAPIView):
    """Контроллер для удаления объекта Question"""
    permission_classes = [IsAuthenticated, IsQuestionOwner]
    queryset = Question.objects.all()
