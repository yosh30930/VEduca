from django.contrib.auth.models import User

from rest_framework import serializers


class ResponsableSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
