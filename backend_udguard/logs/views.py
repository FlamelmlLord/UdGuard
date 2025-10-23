from rest_framework.pagination import PageNumberPagination
from django.db.models.signals import post_save, post_delete
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from logs.serializer import LogsSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.timezone import now
from django.dispatch import receiver
from .models import Logs
from django.apps import apps
from rest_framework import status
import uuid


def log_action(instance, action, user=None, extra_info=""):
    model_name = instance.__class__.__name__.lower()
    
    # Obtener el nombre/título del objeto
    object_name = ""
    if hasattr(instance, 'nombre'):
        # Para indicadores, truncar y agregar el número
        if model_name == 'indicator':
            # Obtener las primeras 4-5 palabras
            words = instance.nombre.split()[:5]
            truncated_name = ' '.join(words)
            if len(words) < len(instance.nombre.split()):
                truncated_name += '...'
            # Agregar el número del indicador
            object_name = f"{truncated_name} (I{instance.id})"
        else:
            object_name = instance.nombre
    elif hasattr(instance, 'titulo'):
        object_name = instance.titulo
    elif hasattr(instance, 'username'):
        object_name = instance.username
    elif hasattr(instance, 'first_name') and hasattr(instance, 'last_name'):
        object_name = f"{instance.first_name} {instance.last_name}".strip() or instance.username
    else:
        object_name = str(instance)
    
    # Para indicadores, agregar la característica padre
    if model_name == 'indicator' and hasattr(instance, 'caracteristica'):
        extra_info = f"de característica 'C{instance.caracteristica.id}. {instance.caracteristica.nombre}'"
    
    # Crear mensaje descriptivo
    if action.lower() == "create":
        accion_text = f"CREAR {model_name.upper()}: '{object_name}'"
    elif action.lower() == "update":
        accion_text = f"ACTUALIZAR {model_name.upper()}: '{object_name}'"
    elif action.lower() == "delete":
        accion_text = f"ELIMINAR {model_name.upper()}: '{object_name}'"
    elif action.lower() == "disable":
        accion_text = f"INHABILITAR {model_name.upper()}: '{object_name}'"
    elif action.lower() == "enable":
        accion_text = f"HABILITAR {model_name.upper()}: '{object_name}'"
    else:
        # Para acciones personalizadas como "login", "upload", etc.
        accion_text = f"{action.upper()}"
        if object_name and model_name != "customuser":
            accion_text += f": '{object_name}'"
    
    # Agregar información extra
    if extra_info:
        accion_text += f" - {extra_info}"

    Logs.objects.create(
        usuario=user,
        accion=accion_text,
    )


class LogsListViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, num_page=25):
        try:
            # ⭐ OBTENER PARÁMETROS DE QUERY PARA FILTROS Y ORDENAMIENTO
            search_query = request.GET.get('search', '').strip()
            sort_field = request.GET.get('sort_field', 'fecha')
            sort_direction = request.GET.get('sort_direction', 'desc')
            
            # ⭐ OBTENER TODOS LOS LOGS CON DATOS DEL USUARIO
            logs = Logs.objects.select_related('usuario').all()
            
            # ⭐ APLICAR FILTROS DE BÚSQUEDA SI EXISTE
            if search_query:
                from django.db.models import Q
                logs = logs.filter(
                    Q(accion__icontains=search_query) |
                    Q(usuario__first_name__icontains=search_query) |
                    Q(usuario__last_name__icontains=search_query) |
                    Q(usuario__username__icontains=search_query) |
                    Q(usuario__email__icontains=search_query)
                )
            
            # ⭐ APLICAR ORDENAMIENTO
            if sort_field == 'usuario':
                # Ordenar por nombre completo del usuario
                if sort_direction == 'desc':
                    logs = logs.order_by('-usuario__first_name', '-usuario__last_name', '-usuario__username')
                else:
                    logs = logs.order_by('usuario__first_name', 'usuario__last_name', 'usuario__username')
            elif sort_field == 'fecha':
                if sort_direction == 'desc':
                    logs = logs.order_by('-fecha')
                else:
                    logs = logs.order_by('fecha')
            elif sort_field == 'accion':
                if sort_direction == 'desc':
                    logs = logs.order_by('-accion')
                else:
                    logs = logs.order_by('accion')
            else:
                # Default ordenar por fecha descendente
                logs = logs.order_by('-fecha')
            
            # ⭐ APLICAR PAGINACIÓN
            paginator = PageNumberPagination()
            paginator.page_size = num_page
            result_page = paginator.paginate_queryset(logs, request)
            serializer = LogsSerializer(result_page, many=True)

            return paginator.get_paginated_response(serializer.data)
            
        except Exception as e:
            print(f"Error en LogsListViewSet: {e}")
            return Response({
                "error": "Error al obtener los logs",
                "detail": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
