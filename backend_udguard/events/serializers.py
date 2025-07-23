from rest_framework import serializers

from events.models import Events


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ["titulo", "descripcion", "fecha_evento"]


class CreateEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ["titulo", "descripcion", "fecha_evento"]

    def create(self, validated_data):
        user = self.context["request"].user
        return Events.objects.create(creado_por=user, **validated_data)
