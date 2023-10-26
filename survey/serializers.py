from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from survey.models import Question, Answer, Survey, WatchedSurvey


class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = ['text']


class QuestionListSerializer(ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['pk', 'survey', 'body', 'answers']


class QuestionAnswerSerializer(ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['body', 'answers']


class SurveySerializer(ModelSerializer):
    questions = QuestionAnswerSerializer(many=True)

    class Meta:
        model = Survey
        fields = ['pk', 'title', 'description', 'questions', 'likes_count', 'views_count', 'published_at', 'author']

    def create(self, validated_data):
        questions = validated_data.pop('questions')

        survey = Survey.objects.create(**validated_data)

        for question_data in questions:
            answers = question_data.pop('answers')
            question = Question.objects.create(survey=survey, **question_data)

            for answer in answers:
                Answer.objects.create(question=question, **answer)

        return survey


class SurveyUpdateSerializer(ModelSerializer):
    questions = QuestionAnswerSerializer(many=True)

    class Meta:
        model = Survey
        fields = ['title', 'description', 'questions']

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)

        questions = validated_data.pop('questions')

        if questions:
            instance.questions.all().delete()

            for question_data in questions:
                answers = question_data.pop('answers')

                question = Question.objects.create(survey=instance, **question_data)

                for answer_data in answers:
                    Answer.objects.create(question=question, **answer_data)

        instance.save()

        return instance


class SurveyListSerializer(ModelSerializer):
    is_watched = SerializerMethodField()

    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'likes_count', 'views_count', 'is_watched']

    def get_is_watched(self, instance):
        user = self.context['request'].user

        user_survey = WatchedSurvey.objects.filter(user=user, survey=instance)

        return user_survey.exists()


class FavoritesSurveySerializer(ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'title', 'likes_count', 'views_count', 'published_at', 'author']


class FavoriteSerializer(ModelSerializer):
    survey = FavoritesSurveySerializer()

    class Meta:
        model = WatchedSurvey
        fields = ['id', 'survey']


class QuestionSerializer(ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['body', 'survey', 'answers']

    def create(self, validated_data):
        answers = validated_data.pop('answers')

        question = Question.objects.create(**validated_data)

        for answer in answers:
            Answer.objects.create(question=question, **answer)

        return question

    def update(self, instance, validated_data):
        instance.body = validated_data.get('body', instance.body)

        new_data = validated_data.pop('answers')

        if new_data:
            instance.answers.all().delete()

            for answer in new_data:
                Answer.objects.create(question=instance, **answer)

        instance.save()

        return instance
