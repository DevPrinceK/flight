from django.shortcuts import render
from django.views import View
from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.utils.decorators import method_decorator
from rest_framework.views import APIView


# @method_decorator(api_view(['GET']))
class HomeAPIView(APIView):
    def get(self, request, *args, **kwargs):
        end_points = {
            'auth': '/api/auth/',
            'users': '/api/users/',
            'groups': '/api/groups/',
            'permissions': '/api/permissions/',
        }
        return Response(end_points)
