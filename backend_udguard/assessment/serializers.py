from rest_framework import serializers
from assessment.models import Factors, Characteristics, Indicator


class FactorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factors
        fields = "__all__"


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
