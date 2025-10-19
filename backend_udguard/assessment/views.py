from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from assessment.models import Factors, Characteristics, Indicator
from assessment.serializers import (
    FactorsSerializer,
    CharacteristicsSerializer,
    IndicatorSerializer,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from logs.views import log_action


class FactorsCreateListViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        factors = Factors.objects.all()
        serializer = FactorsSerializer(factors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        tipo = request.user.tipo_user
        if tipo != "admin":
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        serializer = FactorsSerializer(data=request.data)
        if serializer.is_valid():
            factor = serializer.save()
            log_action(factor, "create", request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FactorsListCreateCharacteristicsViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, __, factors_id):
        characteristics = Characteristics.objects.filter(factors=factors_id)
        data = [characteristic_status(c) for c in characteristics]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, factors_id):
        tipo = request.user.tipo_user
        if tipo != "admin":
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        factor = get_object_or_404(Factors, pk=factors_id)
        data = request.data.copy()
        data["factors"] = factor.id
        serializer = CharacteristicsSerializer(data=data)
        if serializer.is_valid():
            caracteristica = serializer.save()
            log_action(caracteristica, "create", request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CharacteristicListUpdateViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, __, caracteristica_id):
        caracteristica = get_object_or_404(Characteristics, pk=caracteristica_id)
        indicators = Indicator.objects.filter(caracteristica=caracteristica)

        if indicators.exists():
            calificaciones = [
                i.calificacion for i in indicators if i.calificacion is not None
            ]
            promedio = (
                sum(calificaciones) / len(calificaciones) if calificaciones else 0
            )
        else:
            promedio = 0

        caracteristica_data = CharacteristicsSerializer(caracteristica).data
        indicadores_data = IndicatorSerializer(indicators, many=True).data

        caracteristica_data["cumplimiento"] = round(promedio, 1)

        caracteristica_data["porcentaje"] = (
            round(((promedio - 1) / 4) * 100, 1) if promedio else 0
        )

        caracteristica_data["indicadores"] = indicadores_data

        caracteristica_data["grado_cumplimiento"] = get_grado_cumplimiento(
            caracteristica_data["porcentaje"]
        )

        return Response(caracteristica_data, status=status.HTTP_200_OK)

    def patch(self, request, caracteristica_id):
        tipo = request.user.tipo_user
        if tipo != "admin":
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        caracteristica = get_object_or_404(Characteristics, pk=caracteristica_id)
        update_description = request.data["descripcion"]
        if update_description is None:
            return Response(
                {"detail": "El campo 'descripcion' es requerido."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        caracteristica.descripcion = update_description
        log_action(caracteristica, "update", request.user)

        serializer = CharacteristicsSerializer(caracteristica)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, caracteristica_id):
        tipo = request.user.tipo_user
        if tipo != "admin":
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        caracteristica = get_object_or_404(Characteristics, pk=caracteristica_id)
        caracteristica.delete()

        return Response(
            {"message": "Característica e indicadores eliminados"},
            status=status.HTTP_204_NO_CONTENT,
        )


class IndicatorCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, caracteristica_id):
        tipo = request.user.tipo_user
        if tipo != "admin":
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        caracteristica = get_object_or_404(Characteristics, pk=caracteristica_id)
        serializer = IndicatorSerializer(data=request.data)
        if serializer.is_valid():
            indicador = serializer.save(caracteristica=caracteristica)
            log_action(indicador, "create", request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IndicatorUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, indicador_id):
        tipo = request.user.tipo_user
        if tipo != "admin":
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        indicador = get_object_or_404(Indicator, pk=indicador_id)
        serializer = IndicatorSerializer(indicador, data=request.data, partial=True)
        if serializer.is_valid():
            indicador = serializer.save()
            log_action(indicador, "update", request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, indicador_id):
        tipo = request.user.tipo_user
        if tipo != "admin":
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
        indicador = get_object_or_404(Indicator, pk=indicador_id)
        indicador.delete()

        return Response(
            {"message": "indicador eliminado"},
            status=status.HTTP_204_NO_CONTENT,
        )


def get_grado_cumplimiento(porcentaje):
    if 1 < porcentaje < 49:
        return "No se cumple"
    if 50 < porcentaje < 69:
        return "Se cumple insatisfactoriamente"
    if 70 < porcentaje < 79:
        return "Se cumple aceptablemente"
    if porcentaje > 80:
        return "Se cumple en alto grado"


def characteristic_status(caracteristica):
    indicators = Indicator.objects.filter(caracteristica=caracteristica)

    if indicators.exists():
        print(indicators)
        calificaciones = [
            i.calificacion for i in indicators if i.calificacion is not None
        ]
        promedio = sum(calificaciones) / len(calificaciones) if calificaciones else 0
    else:
        promedio = 0

    caracteristica_data = CharacteristicsSerializer(caracteristica).data

    caracteristica_data["cumplimiento"] = round(promedio, 1)
    caracteristica_data["porcentaje"] = (
        round(((promedio - 1) / 4) * 100, 1) if promedio else 0
    )
    caracteristica_data["grado_cumplimiento"] = get_grado_cumplimiento(
        caracteristica_data["porcentaje"]
    )

    return caracteristica_data
