from rest_framework import serializers
from assessment.models import Factors, Characteristics, Indicator

class FactorsSerializer(serializers.ModelSerializer):
    caracteristicas = serializers.SerializerMethodField()
    estado = serializers.SerializerMethodField()
    meta = serializers.SerializerMethodField()
    total_puntajes = serializers.SerializerMethodField()
    cantidad_caracteristicas = serializers.SerializerMethodField()

    class Meta:
        model = Factors
        fields = "__all__"

    def get_caracteristicas(self, obj):
        caracteristicas = obj.characteristics_set.all()[:3]
        return CharacteristicsSerializer(caracteristicas, many=True).data
        
    def get_meta(self, obj):
        caracteristicas = obj.characteristics_set.all()
        if not caracteristicas.exists():
            return 0
        total_metas = 0
        for c in caracteristicas:
            indicadores = c.indicator_set.all()
            total_metas += sum(i.meta for i in indicadores)
        return total_metas

    def get_total_puntajes(self, obj):
        caracteristicas = obj.characteristics_set.all()
        if not caracteristicas.exists():
            return 0
        total_puntajes = 0
        for c in caracteristicas:
            indicadores = c.indicator_set.all()
            total_puntajes += sum(i.puntos for i in indicadores if i.calificacion is not None and i.ponderacion is not None)
        return round(total_puntajes, 2)  # ⭐ CAMBIAR A 2 DECIMALES

    def get_cantidad_caracteristicas(self, obj):
        return obj.characteristics_set.count()

    # ⭐ MÉTODO CORREGIDO PARA CALCULAR GRADO DESDE CARACTERÍSTICAS
    def get_estado(self, obj):
        caracteristicas = obj.characteristics_set.all()
        if not caracteristicas.exists():
            return {
                "grado": "N/A",
                "descripcion": "Sin datos suficientes",
                "color": "#6b7280",
                "promedio": 0.0,
            }

        # ⭐ CALCULAR PROMEDIO DE CADA CARACTERÍSTICA PRIMERO
        cumplimientos_caracteristicas = []
        
        for caracteristica in caracteristicas:
            indicadores = caracteristica.indicator_set.all()
            if indicadores.exists():
                # Obtener calificaciones válidas de los indicadores de esta característica
                calificaciones_indicadores = [
                    i.calificacion for i in indicadores 
                    if i.calificacion is not None
                ]
                
                if calificaciones_indicadores:
                    # Promedio de indicadores para esta característica
                    promedio_caracteristica = sum(calificaciones_indicadores) / len(calificaciones_indicadores)
                    cumplimientos_caracteristicas.append(promedio_caracteristica)

        # ⭐ AHORA CALCULAR EL PROMEDIO DE LAS CARACTERÍSTICAS
        if not cumplimientos_caracteristicas:
            return {
                "grado": "N/A",
                "descripcion": "Sin datos suficientes",
                "color": "#6b7280",
                "promedio": 0.0,
            }

        # ⭐ PROMEDIO DE CARACTERÍSTICAS (NO DE INDICADORES DIRECTAMENTE)
        promedio_factor = sum(cumplimientos_caracteristicas) / len(cumplimientos_caracteristicas)
        promedio_redondeado = round(promedio_factor, 2)  # ⭐ CAMBIAR A 2 DECIMALES

        # ⭐ USAR LA FUNCIÓN EXISTENTE PARA DETERMINAR EL GRADO
        if 1.0 <= promedio_redondeado < 2.5:
            return {
                "grado": "E",
                "descripcion": "No se cumple",
                "color": "#e71000",
                "promedio": promedio_redondeado,
            }
        elif 2.5 <= promedio_redondeado < 3.5:
            return {
                "grado": "D",
                "descripcion": "Se cumple insatisfactoriamente",
                "color": "#e78800",
                "promedio": promedio_redondeado,
            }
        elif 3.5 <= promedio_redondeado < 4.0:
            return {
                "grado": "C",
                "descripcion": "Se cumple aceptablemente",
                "color": "#e7d900",
                "promedio": promedio_redondeado,
            }
        elif 4.0 <= promedio_redondeado < 4.5:
            return {
                "grado": "B",
                "descripcion": "Se cumple en alto grado",
                "color": "#6dca00",
                "promedio": promedio_redondeado,
            }
        elif 4.5 <= promedio_redondeado <= 5.0:
            return {
                "grado": "A",
                "descripcion": "Se cumple plenamente",
                "color": "#00ca00",
                "promedio": promedio_redondeado,
            }
        else:
            return {
                "grado": "N/A",
                "descripcion": "Sin datos suficientes",
                "color": "#6b7280",
                "promedio": promedio_redondeado,
            }

class CharacteristicsSerializer(serializers.ModelSerializer):
    meta = serializers.SerializerMethodField()
    total_puntajes = serializers.IntegerField(read_only=True)
    cantidad_indicadores = serializers.IntegerField(read_only=True)
    cumplimiento = serializers.FloatField(read_only=True)
    porcentaje = serializers.FloatField(read_only=True)
    grado_cumplimiento = serializers.DictField(read_only=True)
    # ⭐ NUEVOS CAMPOS PARA PESO EN FACTOR
    peso_en_factor = serializers.FloatField(read_only=True)
    total_metas_factor = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Characteristics
        fields = "__all__"
        
    def get_meta(self,obj):
        indicadores = obj.indicator_set.all()
        if indicadores.exists():
            return sum(i.meta for i in indicadores)
        return 0


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
