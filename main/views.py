from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Genre, Audio, Comment
from .serializers import GenreSerializer, AudioSerializer, CommentSerializer
from rest_framework import status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

User = get_user_model()


class GenreListCreateView(ListCreateAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class AudioViewSet(viewsets.ViewSet):
    serializer_class  = AudioSerializer
    queryset = Audio.objects.all()
    pagination_class = PageNumberPagination
    # lookup_field = 'email'

    def list(self, request):
        queryset = Audio.objects.filter(visibility='Public')
        pagination = PageNumberPagination()
        qs = pagination.paginate_queryset(queryset, request)
        serializer  = AudioSerializer(qs, many=True)
        return pagination.get_paginated_response(serializer.data)
        # return Response(serializer.data)

    def retrieve(self, request, pk):
        queryset = Audio.objects.all()
        audio = get_object_or_404(queryset, pk=pk)
        serializer = AudioSerializer(audio)
        return Response(serializer.data)


class ListCreateCommentView(ListCreateAPIView): # add a permission_class of isAuthenticated
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
