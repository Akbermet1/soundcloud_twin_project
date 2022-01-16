from rest_framework import serializers
from .models import Audio, Genre, Comment

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
    

class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        exclude = ['likes']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['created_at']