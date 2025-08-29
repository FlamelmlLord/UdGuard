from rest_framework import serializers
from assessment.models import Factors, Characteristics, Indicator


class FactorsSerializer(serializers.ModelSerializer):
    caracteristicas = serializers.SerializerMethodField()
    estado = serializers.SerializerMethodField()
    class Meta:
        model = Factors
        fields = "__all__"

    def get_caracteristicas(self, obj):
        caracteristicas = obj.characteristics_set.all()[:3]
        return CharacteristicsSerializer(caracteristicas, many=True).data
    def get_estado(self, obj):
        caracteristicas = obj.characteristics_set.all()
        Indicadores = Indicator.objects.filter(caracteristica__in=caracteristicas)
        if not Indicadores.exists():
            return {
            "grado": "N/A",
            "descripcion": "Sin datos suficientes",
            "color": "#6b7280",
        }
        suma = sum(Indicadores.values_list('meta', flat=True))
        promedio = suma/Indicadores.count()

        if 1.0 <= promedio <= 2.4:
            return {
            "grado": "E",
            "descripcion": "No se cumple",
            "color": "#e71000",
        }
        elif 2.5 <= promedio <= 3.4:
            return {
            "grado": "D",
            "descripcion": "Se cumple insatisfactoriamente",
            "color": "#e78800",
        }
        elif 3.5 <= promedio <= 3.9:
            return {
            "grado": "C",
            "descripcion": "Se cumple aceptablemente",
            "color": "#e7d900",
        }
        elif 4.0 <= promedio <= 4.4:
            return {
            "grado": "B",
            "descripcion": "Se cumple en alto grado",
            "color": "#6dca00",
        }
        elif 4.5 <= promedio <= 5.0:
            return {
            "grado": "A",
            "descripcion": "Se cumple plenamente",
            "color": "#00ca00",
        }
        else:
            return {
            "grado": "N/A",
            "descripcion": "Sin datos suficientes",
            "color": "#6b7280",
        }

class CharacteristicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristics
        fields = "__all__"


class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = [
            "id",
            "nombre",
            "link_evidencia",
            "ponderacion",
            "meta",
            "calificacion",
            "puntos",
            "porcentaje",
        ]
