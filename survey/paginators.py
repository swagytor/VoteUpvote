from rest_framework.pagination import PageNumberPagination


class SurveyPaginator(PageNumberPagination):
    page_size = 5
