from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, DestroyAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Genre, Audio, Comment
from .serializers import GenreSerializer, AudioSerializer, CommentSerializer
from rest_framework import status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsAuthor

User = get_user_model()


class GenreListCreateView(ListCreateAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class AudioViewSet(viewsets.ModelViewSet): # поменяла на ModelViewSet из-за того, что в ViewSet нету get_object(), который нужен для comments
    serializer_class  = AudioSerializer
    queryset = Audio.objects.all()
    pagination_class = PageNumberPagination
    # lookup_field = 'email'

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action == 'reviews':
            if self.request.method == 'POST' or self.request.method == 'LIST':
                return [IsAuthenticated()]
        return [IsAdminUser()]

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

    # api/v1/products/id/comments/
    @action(['GET', 'POST'], detail=True)
    def comments(self, request, pk=None):
        audio = self.get_object()
        if request.method == 'GET':
            comments = audio.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            data = request.data
            serializer = CommentSerializer(data=data, context={'request': request, 'audio': audio})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        audio = self.get_object()
        data = request.data
        audio.leave_like()
        serializer = CommentSerializer(data=data, context={'request': request, 'audio': audio})
        return Response(serializer.data, status=status.HTTP_200_OK)




class DeleteCommentView(DestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthor]
