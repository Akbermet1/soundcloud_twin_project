from multiprocessing import context
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
        exclude = ['created_at', 'user', 'audio']

    def create(self, validated_data):
        audio = self.context.get('audio')
        user = self.context.get('request').user
        validated_data['user'] = user
        validated_data['audio'] = audio
        return super().create(validated_data)