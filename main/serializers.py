from rest_framework import serializers
from .models import Audio, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
    

class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        exclude = ['likes']