from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.views import APIView
from rest_framework import status,generics, viewsets, serializers
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.decorators import action

from actstream.models import Action

class ListActivityView(APIView):
    """
    View to list all activities
    """
    def get(self, request, format=None):
        return Response({'activities':[str(action) for action in Action.objects.all()]}, status=status.HTTP_200_OK)

