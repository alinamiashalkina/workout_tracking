from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    repeat_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "repeat_password",
            "role"
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        role = validated_data.get("role")

        # Создать админа можно только через админку или createsuperuser
        if role == User.Role.ADMIN:
            raise PermissionDenied(
                "You cannot create an Admin."
            )

        password = validated_data["password"]
        repeat_password = validated_data.pop("repeat_password")
        if password != repeat_password:
            raise serializers.ValidationError(
                {"password": "The two password fields must match."})
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(**attrs)
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        return user
