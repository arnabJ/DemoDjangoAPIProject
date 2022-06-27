from django.contrib.auth.models import User
from rest_framework import serializers

from apiV1.models import Address


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password')
        )
        return user


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email"]


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = "__all__"

    def __str__(self):
        return f"{self.line_one}, {self.line_two}, {self.city}, {self.state}, {self.country}-{self.zip_code}({self.id})"
