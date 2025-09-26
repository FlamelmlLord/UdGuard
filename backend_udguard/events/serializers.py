from rest_framework import serializers

from events.models import Events
from users.serializers import UserListSerializer


class EventsSerializer(serializers.ModelSerializer):
    creado_por = UserListSerializer(read_only=True)
    tipo_evento_display = serializers.CharField(source='get_tipo_evento_display', read_only=True)
    
    class Meta:
        model = Events
        fields = [
            "id", "titulo", "descripcion", "fecha_inicio", "fecha_fin", 
            "tipo_evento", "tipo_evento_display", "creado_por"
        ]
        read_only_fields = ["id", "creado_por", "fecha_creacion"]


class CreateEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ["titulo", "descripcion", "fecha_inicio", "fecha_fin", "tipo_evento"]
        
    def validate(self, data):
        # Validar que la fecha de fin sea posterior a la de inicio
        if data.get('fecha_fin') and data.get('fecha_inicio'):
            if data['fecha_fin'] <= data['fecha_inicio']:
                raise serializers.ValidationError(
                    "La fecha de fin debe ser posterior a la fecha de inicio."
                )
        
        # Validar longitud del título
        if len(data.get('titulo', '')) > 100:
            raise serializers.ValidationError(
                "El título no puede exceder 100 caracteres."
            )
            
        # Validar longitud de la descripción
        if len(data.get('descripcion', '')) > 500:
            raise serializers.ValidationError(
                "La descripción no puede exceder 500 caracteres."
            )
        
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        return Events.objects.create(creado_por=user, **validated_data)


class UpdateEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ["titulo", "descripcion", "fecha_inicio", "fecha_fin", "tipo_evento"]
        
    def validate(self, data):
        # Mismas validaciones que en Create
        if data.get('fecha_fin') and data.get('fecha_inicio'):
            if data['fecha_fin'] <= data['fecha_inicio']:
                raise serializers.ValidationError(
                    "La fecha de fin debe ser posterior a la fecha de inicio."
                )
        
        if len(data.get('titulo', '')) > 100:
            raise serializers.ValidationError(
                "El título no puede exceder 100 caracteres."
            )
            
        if len(data.get('descripcion', '')) > 500:
            raise serializers.ValidationError(
                "La descripción no puede exceder 500 caracteres."
            )
        
        return data
