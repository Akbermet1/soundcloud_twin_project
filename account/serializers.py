from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=6,
        style={'input_type': 'password'},
        required=True
    )
    password_confirm = serializers.CharField(
        min_length=6,
        style={'input_type': 'password'},
        required=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'age', 'password', 'password_confirm')

    def validate(self, validated_data):
        password = validated_data.get('password')
        password_confirm = validated_data.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('passwords must match!')
        return validated_data

    def create(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        password = validated_data.get('password')
        age = validated_data.get('age')
        print(f'PASSSWORD: {password}')
        user = User.objects.create_user(email=email, username=username, age=age, password=password)
        user.assign_activation_code()
        print('activation_code: ',user.activation_code)
        user.send_activation_email(action='register')
        user.save()
        return user