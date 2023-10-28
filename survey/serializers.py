from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from survey import services
from survey.models import Question, Survey, WatchedSurvey, Choice


class SurveySerializer(ModelSerializer):
    """Сериалайзер для просмотра краткой информации об опросе"""
    is_watched = SerializerMethodField()

    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'likes_count', 'views_count', 'is_watched']

    def get_is_watched(self, instance):
        """Метод проверки чтения данного опроса раньше"""
        user = self.context['request'].user

        user_survey = WatchedSurvey.objects.filter(user=user, survey=instance)

        return user_survey.exists()


class FavoriteSerializer(ModelSerializer):
    """Сериалайзер для вывода лайкнутых опросов"""
    survey = SurveySerializer()

    class Meta:
        model = WatchedSurvey
        fields = ['id', 'survey']


class ChoiceSerializer(ModelSerializer):
    """Сериалайзер для вывода вариантов ответа"""
    class Meta:
        model = Choice
        fields = ['option']


class QuestionSerializer(ModelSerializer):
    """Сериалайзер для вывода информации о вопросах"""
    choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ['pk', 'question', 'choices', 'answer']
        write_only_fields = ['question', 'choices', 'answer']

    def create(self, validated_data):
        """Переопределённый метод создания объекта Question, а также его вложенностей"""
        survey = validated_data.get('survey')

        question = services.validate_new_question(survey, validated_data)

        return question

    def update(self, instance, validated_data):
        """Переопределённый метод обновления объекта Question, а также его вложенностей"""
        choices = None

        instance.question = validated_data.get('question', instance.question)
        instance.answer = validated_data.get('answer', instance.answer)

        if validated_data.get('choices'):
            choices = validated_data.pop('choices')

        if choices is not None:
            instance.choices.all().delete()

            for option in choices:
                Choice.objects.create(question=instance, **option)

        instance.save()

        return instance


class CreateQuestionSerializer(ModelSerializer):
    """Сериалайзер для создания объекта Question"""
    choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ['pk', 'question', 'choices', 'survey', 'answer']
        write_only_fields = ['question', 'choices', 'answer']

    def create(self, validated_data):
        """Переопределённый метод создания объекта Question с уже существующим Survey"""
        survey = validated_data.pop('survey')

        question = services.validate_new_question(survey, validated_data)

        return question


class SurveyQuestionSerializer(ModelSerializer):
    """Сериалайзер для вывода полной информации об конкретном опросе со всеми его вопросами и вариантами ответа"""
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = ['pk', 'title', 'description', 'questions', 'likes_count', 'views_count', 'published_at', 'author']
        write_only_fields = ['title', 'description', 'questions']

    def create(self, validated_data):
        """Переопределённый метод создания объекта Survey, а также его вложенностей"""
        questions = validated_data.pop('questions')

        survey = Survey.objects.create(**validated_data)

        for question_data in questions:
            services.validate_new_question(survey, question_data)

        return survey


class SurveyUpdateSerializer(ModelSerializer):
    """Сериалайзер для обновления объекта Survey"""
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Survey
        fields = ['title', 'description', 'questions']

    def update(self, instance, validated_data):
        """Переопределённый метод обновления объекта Survey, а также его вложенностей"""
        instance.title = validated_data.get('title')
        instance.description = validated_data.get('description', instance.description)

        if validated_data.get('questions'):
            questions_data = validated_data.pop('questions')

            services.validate_questions(instance, questions_data)

        instance.save()

        return instance
