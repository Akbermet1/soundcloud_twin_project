from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Genre, Audio
from .serializers import GenreSerializer, AudioSerializer
from rest_framework import status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


User = get_user_model()


class GenreListCreateView(ListCreateAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class AudioViewSet(viewsets.ViewSet):
    serializer_class  = AudioSerializer
    queryset = Audio.objects.all()

    def list(self, request):
        queryset = Audio.objects.filter(visibility='Public')
        serializer  = AudioSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        user = get_object_or_404(User, email=pk)
        queryset = user.audios
        serializer = AudioSerializer(queryset, many=True)
        return Response(serializer.data)
