from multiprocessing import context
from rest_framework import serializers
from .models import Audio, Genre, Comment
import io
from rest_framework.parsers import JSONParser


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
    

class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        exclude = ['likes', 'uploader']

    def create(self, validated_data):
        user = self.context.get('uploader')
        validated_data['uploader'] = user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['created_at', 'user', 'audio']

    def create(self, validated_data):
        audio = self.context.get('audio')
        user = self.context.get('request').user
        validated_data['user'] = user
        validated_data['audio'] = audio
        return super().create(validated_data)