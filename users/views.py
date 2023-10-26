from django.conf import settings
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from survey.models import WatchedSurvey
from survey.serializers import FavoriteSerializer


# Create your views here.
@api_view(['GET'])
def vk_authentication(request):
    return Response({
        "url": f"https://login.vk.com/?act=openapi&oauth=1&aid={settings.SOCIAL_AUTH_VK_OAUTH2_KEY}&location=127.0.0.1&new=1&response_type=code"},
        status=status.HTTP_200_OK, )


class FavoritesSurveyListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer
    queryset = WatchedSurvey.objects.all()

    def get_queryset(self):
        user = self.request.user

        queryset = super().get_queryset()

        queryset = queryset.filter(user=user, like_or_dislike='like')

        return queryset
