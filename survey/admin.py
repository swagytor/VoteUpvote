from django.contrib import admin

from survey.models import Survey, Question, Choice


# Register your models here.
@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'likes_count', 'views_count', 'published_at', 'author']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["pk", "question", "survey"]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["pk", "option", "question"]
