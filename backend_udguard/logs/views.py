from rest_framework.pagination import PageNumberPagination
from django.db.models.signals import post_save, post_delete
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from logs.serializer import LogsSerializer
from rest_framework.views import APIView
from django.utils.timezone import now
from django.dispatch import receiver
from .models import Logs
from django.apps import apps
import uuid


def log_action(instance, action, user=None):
    model_name = instance.__class__.__name__.lower()

    Logs.objects.create(
        usuario=user,
        accion=f"{action.upper()} {model_name}",
    )


class LogsListViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, num_page=5):
        logs = Logs.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = num_page
        result_page = paginator.paginate_queryset(logs, request)
        serializer = LogsSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
