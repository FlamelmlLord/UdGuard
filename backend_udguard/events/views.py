from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from events.serializers import EventsSerializer, CreateEventsSerializer, UpdateEventsSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from events.models import Events
from logs.views import log_action
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta


class EventsListCreateViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, num_page=25):
        """
        Obtener lista de eventos con filtros opcionales
        """
        try:
            # Obtener parámetros de query
            search_query = request.GET.get('search', '').strip()
            event_type = request.GET.get('type', '')
            start_date = request.GET.get('start_date', '')
            end_date = request.GET.get('end_date', '')
            
            # Obtener todos los eventos
            events = Events.objects.select_related('creado_por').all()
            
            # Aplicar filtros
            if search_query:
                from django.db.models import Q
                events = events.filter(
                    Q(titulo__icontains=search_query) |
                    Q(descripcion__icontains=search_query)
                )
            
            if event_type:
                events = events.filter(tipo_evento=event_type)
            
            if start_date:
                try:
                    start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
                    events = events.filter(fecha_inicio__date__gte=start_dt)
                except ValueError:
                    pass
            
            if end_date:
                try:
                    end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
                    events = events.filter(fecha_inicio__date__lte=end_dt)
                except ValueError:
                    pass
            
            # Ordenar por fecha de inicio
            events = events.order_by('fecha_inicio')
            
            # Aplicar paginación
            paginator = PageNumberPagination()
            paginator.page_size = num_page
            result_page = paginator.paginate_queryset(events, request)
            serializer = EventsSerializer(result_page, many=True)

            return paginator.get_paginated_response(serializer.data)
            
        except Exception as e:
            print(f"Error en EventsListCreateViewSet.get: {e}")
            return Response({
                "error": "Error al obtener los eventos",
                "detail": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        Crear nuevo evento (solo para administradores)
        """
        try:
            tipo = request.user.tipo_user
            if tipo != "admin":
                return Response({
                    "error": "No tienes permisos para crear eventos"
                }, status=status.HTTP_403_FORBIDDEN)

            print(f"Datos recibidos para crear evento: {request.data}")

            serializer = CreateEventsSerializer(
                data=request.data, 
                context={"request": request}
            )
            
            if serializer.is_valid():
                evento = serializer.save()
                
                # ⭐ LOG MEJORADO CON FECHA Y TIPO DE EVENTO
                fecha_evento = evento.fecha_inicio.strftime('%Y-%m-%d %H:%M')
                tipo_evento_display = dict(Events.TIPO_EVENTO_CHOICES).get(evento.tipo_evento, evento.tipo_evento)
                extra_info = f"tipo: {tipo_evento_display}, fecha: {fecha_evento}"
                log_action(evento, "create", request.user, extra_info)
                
                # Devolver el evento creado con todos los datos
                response_serializer = EventsSerializer(evento)
                
                print(f"Evento creado exitosamente: {evento.id}")
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(f"Errores de validación: {serializer.errors}")
                return Response({
                    "error": "Datos inválidos",
                    "details": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            print(f"Error creando evento: {e}")
            return Response({
                "error": "Error interno al crear el evento",
                "detail": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventDetailViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        """
        Obtener detalles de un evento específico
        """
        try:
            evento = get_object_or_404(Events, pk=event_id)
            serializer = EventsSerializer(evento)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": "Error al obtener el evento",
                "detail": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, event_id):
        """
        Actualizar evento completo (solo administradores)
        """
        try:
            if request.user.tipo_user != "admin":
                return Response({
                    "error": "No tienes permisos para editar eventos"
                }, status=status.HTTP_403_FORBIDDEN)

            evento = get_object_or_404(Events, pk=event_id)
            
            print(f"Actualizando evento {event_id} con datos: {request.data}")
            
            serializer = UpdateEventsSerializer(
                evento, 
                data=request.data, 
                partial=False
            )
            
            if serializer.is_valid():
                updated_evento = serializer.save()
                
                # ⭐ LOG MEJORADO CON FECHA Y TIPO
                fecha_evento = updated_evento.fecha_inicio.strftime('%Y-%m-%d %H:%M')
                tipo_evento_display = dict(Events.TIPO_EVENTO_CHOICES).get(updated_evento.tipo_evento, updated_evento.tipo_evento)
                extra_info = f"tipo: {tipo_evento_display}, fecha: {fecha_evento}"
                log_action(updated_evento, "update", request.user, extra_info)
                
                # Devolver evento actualizado
                response_serializer = EventsSerializer(updated_evento)
                
                print(f"Evento actualizado exitosamente: {event_id}")
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                print(f"Errores de validación en actualización: {serializer.errors}")
                return Response({
                    "error": "Datos inválidos",
                    "details": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            print(f"Error actualizando evento: {e}")
            return Response({
                "error": "Error interno al actualizar el evento",
                "detail": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, event_id):
        """
        Actualizar evento parcial (solo administradores)
        """
        try:
            if request.user.tipo_user != "admin":
                return Response({
                    "error": "No tienes permisos para editar eventos"
                }, status=status.HTTP_403_FORBIDDEN)

            evento = get_object_or_404(Events, pk=event_id)
            
            serializer = UpdateEventsSerializer(
                evento, 
                data=request.data, 
                partial=True
            )
            
            if serializer.is_valid():
                updated_evento = serializer.save()
                
                # ⭐ LOG MEJORADO
                fecha_evento = updated_evento.fecha_inicio.strftime('%Y-%m-%d %H:%M')
                tipo_evento_display = dict(Events.TIPO_EVENTO_CHOICES).get(updated_evento.tipo_evento, updated_evento.tipo_evento)
                extra_info = f"tipo: {tipo_evento_display}, fecha: {fecha_evento}"
                log_action(updated_evento, "update", request.user, extra_info)
                
                response_serializer = EventsSerializer(updated_evento)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({
                    "error": "Datos inválidos",
                    "details": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                "error": "Error interno al actualizar el evento",
                "detail": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, event_id):
        """
        Eliminar evento (solo administradores)
        """
        try:
            if request.user.tipo_user != "admin":
                return Response({
                    "error": "No tienes permisos para eliminar eventos"
                }, status=status.HTTP_403_FORBIDDEN)

            evento = get_object_or_404(Events, pk=event_id)
            
            # ⭐ GUARDAR INFORMACIÓN PARA EL LOG ANTES DE ELIMINAR
            evento_titulo = evento.titulo
            fecha_evento = evento.fecha_inicio.strftime('%Y-%m-%d %H:%M')
            tipo_evento_display = dict(Events.TIPO_EVENTO_CHOICES).get(evento.tipo_evento, evento.tipo_evento)
            extra_info = f"tipo: {tipo_evento_display}, fecha: {fecha_evento}"
            
            # ⭐ LOG ANTES DE ELIMINAR
            log_action(evento, "delete", request.user, extra_info)
            
            evento.delete()
            
            print(f"Evento eliminado exitosamente: {evento_titulo}")
            return Response({
                "message": "Evento eliminado correctamente"
            }, status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            print(f"Error eliminando evento: {e}")
            return Response({
                "error": "Error interno al eliminar el evento",
                "detail": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventStatsViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Obtener estadísticas de eventos para el dashboard
        """
        try:
            now = timezone.now()
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1)
            
            # Eventos totales
            total_events = Events.objects.count()
            
            # Eventos de hoy
            today_events = Events.objects.filter(
                fecha_inicio__range=[today_start, today_end]
            ).count()
            
            # Eventos próximos (próximos 30 días)
            future_events = Events.objects.filter(
                fecha_inicio__gte=now,
                fecha_inicio__lte=now + timedelta(days=30)
            ).count()
            
            # Eventos por tipo
            events_by_type = {}
            for tipo, display in Events.TIPO_EVENTO_CHOICES:
                count = Events.objects.filter(tipo_evento=tipo).count()
                events_by_type[tipo] = {
                    'count': count,
                    'display': display
                }
            
            return Response({
                'total_events': total_events,
                'today_events': today_events,
                'upcoming_events': future_events,
                'events_by_type': events_by_type
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"Error obteniendo estadísticas de eventos: {e}")
            return Response({
                "error": "Error al obtener estadísticas",
                "detail": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
