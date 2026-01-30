from rest_framework import serializers
from .models import Account

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class MeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    email = serializers.EmailField()
    role = serializers.CharField()
    year = serializers.IntegerField()
    submissions_this_year = serializers.IntegerField()
    remaining_this_year = serializers.IntegerField()
