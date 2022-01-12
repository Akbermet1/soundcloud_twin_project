from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serilizer = RegisterSerializer(data=data)
        serilizer.is_valid(raise_exception=True)
        serilizer.save()
        return Response("You've been successfully registered", status=status.HTTP_201_CREATED)
