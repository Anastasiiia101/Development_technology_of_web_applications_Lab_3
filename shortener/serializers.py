from rest_framework import serializers
from shortener import models


class URLSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        fields = (
            'id',
            'original_url',
            'short_url',
            'name',
            'owner',
        )
        model = models.URL


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = (
            'id',
            'username',
            'email',
            'birthday',
            'gender',
        )
