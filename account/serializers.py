from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth.base_user import BaseUserManager


User = get_user_model()

def normalize_email(email):
    """
    Normalize the email address by lowercasing the domain part of it.
    """
    email = email or ''
    try:
        email_name, domain_part = email.strip().rsplit('@', 1)
    except ValueError:
        pass
    else:
        email = email_name + '@' + domain_part.lower()
    return email


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
    avatar = serializers.ImageField(required=False)
    background_image = serializers.ImageField(required=False)


    class Meta:
        model = User
        fields = ('email', 'username', 'age', 'password', 'password_confirm', 'avatar', 'background_image')

    def validate_age(self, age):
        if age < 16:
            raise serializers.ValidationError('Sorry, but individuals under 16 cannot register on our platform')
        return age

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
        avatar = None
        if validated_data.get('avatar'):
            avatar = validated_data.get('avatar')
        background_image = None
        if validated_data.get('background_image'):
            background_image = validated_data.get('background_image')
        print(f'PASSSWORD: {password}')
        user = User.objects.create_user(email=email, username=username, age=age, password=password, avatar=avatar, background_image=background_image)
        user.assign_activation_code()
        print('activation_code: ',user.activation_code)
        user.send_activation_email(action='register')
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, required=True)

    def validate_email(self, email):
        email = normalize_email(email)

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return email

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = User.objects.get(email=email)

        if not user.check_password(password):
            raise serializers.ValidationError('Wrong password')

        if not user.is_active:
            return serializers.ValidationError('Please, activate your account in order to be able to login')
        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(min_length=6, required=True)
    new_password = serializers.CharField(min_length=6, required=True)
    new_password_confirmation = serializers.CharField(min_length=6, required=True)

    def validate_current_password(self, current_password):
        print('self.context:', self.context)
        user = self.context.get('request').user
        if not user.check_password(current_password):
            raise serializers.ValidationError("The password you've entered doesn't match your current password")
        return current_password

    def validate(self, validated_data):
        new_password = validated_data.get('new_password')
        new_password_confirmation = validated_data.get('new_password_confirmation')
        if new_password != new_password_confirmation:
            raise serializers.ValidationError("The new password and its confirmation don't match")
        return validated_data
    
    def set_new_password(self):
        new_password = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_password)
        user.save()