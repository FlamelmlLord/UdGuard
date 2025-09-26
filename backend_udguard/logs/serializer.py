from rest_framework import serializers
from .models import Logs
from users.serializers import UserListSerializer


class LogsSerializer(serializers.ModelSerializer):
    usuario = UserListSerializer(read_only=True)

    class Meta:
        model = Logs
        fields = ["id", "accion", "fecha", "usuario"]
