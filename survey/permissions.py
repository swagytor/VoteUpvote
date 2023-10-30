from rest_framework.permissions import BasePermission


class IsSurveyOwner(BasePermission):
    """Является ли пользователем автором опроса"""
    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'destroy']:
            user = request.user

            return obj.author == user

        return True


class IsQuestionOwner(BasePermission):
    """Является ли пользователем автором вопроса"""
    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'destroy']:
            user = request.user

            return obj.survey.author == user

        return True
