from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password", "age"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_age(self, value):
        age = int(value)
        if age < 15:
            raise serializers.ValidationError(
                "The person has to be at least 15 years old."
            )
        return age

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
