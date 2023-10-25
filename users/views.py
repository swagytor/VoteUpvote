import requests
from django.conf import settings
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from oauth2_provider.models import Application
from rest_framework.reverse import reverse


# Create your views here.
@api_view(['GET'])
def vk_authentication(request):
    return Response({
        "url": f"https://login.vk.com/?act=openapi&oauth=1&aid={settings.SOCIAL_AUTH_VK_OAUTH2_KEY}&location=127.0.0.1&new=1&response_type=code"},
        status=status.HTTP_200_OK, )

