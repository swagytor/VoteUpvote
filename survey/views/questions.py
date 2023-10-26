from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from survey.models import Question
from survey.permissions import IsQuestionOwner
from survey.serializers import QuestionListSerializer, QuestionSerializer


class QuestionCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer


class QuestionListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionListSerializer
    queryset = Question.objects.all()


class QuestionRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class QuestionUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsQuestionOwner]
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class QuestionDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsQuestionOwner]
    queryset = Question.objects.all()
