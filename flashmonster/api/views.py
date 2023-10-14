from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import permissions


from flashmonster.api.models import AppUser, Word, Examples
from flashmonster.api.serializers import AppUserSerializer, WordSerializer

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. This backend is working.")

from rest_framework import generics

generics.ListCreateAPIView
generics.RetrieveAPIView

class ListUsers(APIView):

    def post(self, request, format=None):
        # create user
        serializer = AppUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
