import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
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

    def patch(self, request):
        tipo = request.user.tipo_user
        if tipo != "admin":
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        factor_id = request.data.get("id")
        if not factor_id:
            return Response({"error": "Debe enviar el id del factor a actualizar"}, status=status.HTTP_400_BAD_REQUEST)

        factor = get_object_or_404(Factors, pk=factor_id)
        factor.nombre = request.data.get("nombre", factor.nombre)
        factor.descripcion = request.data.get("descripcion", factor.descripcion)
        factor.save(update_fields=["nombre", "descripcion"])

        log_action(factor, "update", request.user)

        return Response({"message": "Factor actualizado correctamente"}, status=status.HTTP_200_OK)

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

    def get(self, request, caracteristica_id):
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
            caracteristica_data["cumplimiento"]
        )

        return Response(caracteristica_data, status=status.HTTP_200_OK)

    def patch(self, request, caracteristica_id):
        tipo = request.user.tipo_user
        if tipo != "admin":
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        caracteristica = get_object_or_404(Characteristics, pk=caracteristica_id)
        update_name = request.data["nombre"]
        update_description = request.data["descripcion"]
        if update_description is None and update_name is None:
            return Response(
                {"detail": "El campo 'nombre' y 'descripcion' son requeridos."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        caracteristica.nombre = update_name
        caracteristica.descripcion = update_description
        log_action(caracteristica, "update", request.user)
        caracteristica.save()
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

def get_grado_cumplimiento(grado_numerico):
    """
    Determina el grado de cumplimiento basado en la escala numérica 1-5
    según la tabla de evaluación institucional
    """
    if 1.0 <= grado_numerico <= 2.4:
        return {
            "grado": "E",
            "descripcion": "No se cumple",
            "color": "#e71000",
        }
    elif 2.5 <= grado_numerico <= 3.4:
        return {
            "grado": "D",
            "descripcion": "Se cumple insatisfactoriamente",
            "color": "#e78800",
        }
    elif 3.5 <= grado_numerico <= 3.9:
        return {
            "grado": "C",
            "descripcion": "Se cumple aceptablemente",
            "color": "#e7d900",
        }
    elif 4.0 <= grado_numerico <= 4.4:
        return {
            "grado": "B",
            "descripcion": "Se cumple en alto grado",
            "color": "#6dca00",
        }
    elif 4.5 <= grado_numerico <= 5.0:
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


def calcular_porcentaje_desde_grado(
    grado_numerico, min_puntaje=1.0, max_puntaje=5.0
):
    """
    Convierte el grado numérico (1-5) a porcentaje (0-100%)
    """
    if grado_numerico is None or grado_numerico == 0:
        return 0

    # Normalizar a escala 0-100
    porcentaje = ((grado_numerico - min_puntaje) / (max_puntaje - min_puntaje)) * 100
    return round(porcentaje, 1)

# Actualiza la función characteristic_status para incluir los totales calculados
def characteristic_status(caracteristica):
    indicators = Indicator.objects.filter(caracteristica=caracteristica)

    if indicators.exists():
        print(indicators)
        calificaciones = [
            i.calificacion for i in indicators if i.calificacion is not None
        ]
        promedio = sum(calificaciones) / len(calificaciones) if calificaciones else 0
        
        # ⭐ AGREGAR CÁLCULOS DE TOTALES (igual que en factores)
        total_metas = sum(i.meta for i in indicators if i.meta is not None)
        total_puntajes = sum(i.puntos for i in indicators if i.calificacion is not None and i.ponderacion is not None)
        
    else:
        promedio = 0
        total_metas = 0
        total_puntajes = 0

    caracteristica_data = CharacteristicsSerializer(caracteristica).data

    caracteristica_data["cumplimiento"] = round(promedio, 1)
    caracteristica_data["porcentaje"] = (
        round(((promedio - 1) / 4) * 100, 1) if promedio else 0
    )
    caracteristica_data["grado_cumplimiento"] = get_grado_cumplimiento(
        caracteristica_data["cumplimiento"]
    )
    
    # ⭐ AGREGAR TOTALES A LA RESPUESTA (igual que en factores)
    caracteristica_data["total_metas"] = total_metas
    caracteristica_data["total_puntajes"] = total_puntajes
    caracteristica_data["cantidad_indicadores"] = indicators.count()

    return caracteristica_data

# ⭐ NUEVA CLASE PARA PROCESAR ENCUESTAS
class SurveyUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:
            # Validar que el usuario tenga permisos
            if request.user.tipo_user != "admin":
                return Response(
                    {"error": "No tienes permisos para subir encuestas"}, 
                    status=status.HTTP_403_FORBIDDEN
                )

            # Obtener archivo y tipo de encuesta
            uploaded_file = request.FILES.get('file')
            survey_type = request.data.get('survey_type')

            if not uploaded_file:
                return Response(
                    {"error": "No se ha proporcionado ningún archivo"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not survey_type:
                return Response(
                    {"error": "Debe especificar el tipo de encuesta"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validar extensión del archivo
            file_extension = uploaded_file.name.lower().split('.')[-1]
            if file_extension not in ['xlsx', 'xls', 'csv']:
                return Response(
                    {"error": "Formato de archivo no válido. Solo se permiten archivos Excel (.xlsx, .xls) o CSV"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Procesar el archivo Excel
            survey_data = self.process_excel_file(uploaded_file, survey_type)
            
            if not survey_data:
                return Response(
                    {"error": "No se pudieron extraer datos del archivo"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Guardar como JSON
            json_filename = self.save_survey_json(survey_data, survey_type)

            # ⭐ LOG CORREGIDO
            from logs.models import Logs
            Logs.objects.create(
                usuario=request.user,
                accion=f"UPLOAD encuesta_{survey_type} - {uploaded_file.name}",
            )

            return Response({
                "message": "Archivo procesado exitosamente",
                "survey_type": survey_type,
                "questions_processed": len(survey_data),
                "json_file": json_filename,
                "total_responses": sum(
                    sum(value for key, value in q.items() if key != "Pregunta" and isinstance(value, (int, float)))
                    for q in survey_data
                )
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error processing survey: {e}")
            return Response(
                {"error": f"Error interno al procesar el archivo: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def process_excel_file(self, uploaded_file, survey_type):
        """
        Procesa el archivo Excel y extrae preguntas y respuestas
        """
        try:
            print(f"=== INICIANDO PROCESAMIENTO DE ARCHIVO ===")
            print(f"Nombre del archivo: {uploaded_file.name}")
            print(f"Tamaño del archivo: {uploaded_file.size} bytes")
            print(f"Tipo de encuesta: {survey_type}")
            
            # ⭐ LEER EL ARCHIVO CON CODIFICACIÓN ESPECÍFICA
            if uploaded_file.name.lower().endswith('.csv'):
                print("Procesando como archivo CSV")
                # Para CSV, especificar encoding UTF-8
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            else:
                print("Procesando como archivo Excel")
                # ⭐ USAR OPENPYXL ENGINE QUE MANEJA MEJOR UTF-8
                df = pd.read_excel(uploaded_file, sheet_name=0, header=None, engine='openpyxl')

            print(f"Dimensiones del DataFrame: {df.shape}")
            print(f"Primeras 5 filas del DataFrame:")
            print(df.head())
            
            # Verificar si el DataFrame está vacío
            if df.empty:
                print("ERROR: El DataFrame esta vacio")
                return None

            survey_data = []
            
            # Obtener las preguntas de la primera fila (fila 0)
            if len(df) == 0:
                print("ERROR: No hay filas en el DataFrame")
                return None
                
            questions_row = df.iloc[0]
            print(f"Fila de preguntas completa: {len(questions_row)} columnas")
            
            # Filtrar preguntas válidas (no NaN y no vacías)
            questions = []
            for i, question in enumerate(questions_row):
                if pd.notna(question) and str(question).strip():
                    questions.append((i, str(question).strip()))
                    print(f"Pregunta valida en columna {i}: '{str(question).strip()[:80]}...'")
            
            print(f"Total de preguntas validas encontradas: {len(questions)}")
            
            if not questions:
                print("ERROR: No se encontraron preguntas validas en la primera fila")
                return None

            # Procesar cada pregunta (columna)
            for col_index, question in questions:
                print(f"\n--- Procesando columna {col_index}: {question[:50]}... ---")
                
                # Obtener las respuestas de esta columna (desde fila 1 en adelante)
                if len(df) <= 1:
                    print(f"WARNING: No hay datos de respuesta para la columna {col_index}")
                    continue
                    
                responses_column = df.iloc[1:, col_index]
                print(f"Total respuestas brutas en columna {col_index}: {len(responses_column)}")
                
                # Filtrar respuestas válidas
                responses = [
                    response for response in responses_column 
                    if pd.notna(response) and str(response).strip()
                ]
                
                print(f"Total de respuestas validas en columna {col_index}: {len(responses)}")
                print(f"Primeras 5 respuestas: {responses[:5]}")
                
                if not responses:
                    print(f"WARNING: No hay respuestas validas para la pregunta en columna {col_index}")
                    continue
                
                # Contar las respuestas según las opciones predefinidas
                response_counts = {
                    "Pregunta": question,
                    "1. No tengo información o conocimiento": 0,
                    "2. Totalmente en desacuerdo": 0,
                    "3. En desacuerdo": 0,
                    "4. De acuerdo": 0,
                    "5. Totalmente de acuerdo": 0
                }

                # ⭐ MAPEO AMPLIADO PARA INCLUIR LAS RESPUESTAS EXACTAS DEL ARCHIVO
                response_mapping = {
                    # ⭐ VARIACIONES CON NÚMEROS Y PUNTOS (formato del archivo)
                    "1. no tengo información o conocimiento": "1. No tengo información o conocimiento",
                    "1. no tengo informacion o conocimiento": "1. No tengo información o conocimiento",
                    "2. totalmente en desacuerdo": "2. Totalmente en desacuerdo",
                    "3. en desacuerdo": "3. En desacuerdo", 
                    "4. de acuerdo": "4. De acuerdo",
                    "5. totalmente de acuerdo": "5. Totalmente de acuerdo",
                    
                    # Variaciones sin números
                    "1": "1. No tengo información o conocimiento",
                    "1.0": "1. No tengo información o conocimiento",
                    "no tengo información": "1. No tengo información o conocimiento",
                    "no tengo informacion": "1. No tengo información o conocimiento",
                    "sin información": "1. No tengo información o conocimiento",
                    "sin informacion": "1. No tengo información o conocimiento",
                    "no sé": "1. No tengo información o conocimiento",
                    "no se": "1. No tengo información o conocimiento",
                    "ns/nc": "1. No tengo información o conocimiento",
                    
                    # Variaciones para "Totalmente en desacuerdo"
                    "2": "2. Totalmente en desacuerdo",
                    "2.0": "2. Totalmente en desacuerdo",
                    "totalmente en desacuerdo": "2. Totalmente en desacuerdo",
                    "muy en desacuerdo": "2. Totalmente en desacuerdo",
                    "completamente en desacuerdo": "2. Totalmente en desacuerdo",
                    
                    # Variaciones para "En desacuerdo"
                    "3": "3. En desacuerdo",
                    "3.0": "3. En desacuerdo",
                    "en desacuerdo": "3. En desacuerdo",
                    "desacuerdo": "3. En desacuerdo",
                    
                    # Variaciones para "De acuerdo"
                    "4": "4. De acuerdo",
                    "4.0": "4. De acuerdo",
                    "de acuerdo": "4. De acuerdo",
                    "acuerdo": "4. De acuerdo",
                    
                    # Variaciones para "Totalmente de acuerdo"
                    "5": "5. Totalmente de acuerdo",
                    "5.0": "5. Totalmente de acuerdo",
                    "totalmente de acuerdo": "5. Totalmente de acuerdo",
                    "muy de acuerdo": "5. Totalmente de acuerdo",
                    "completamente de acuerdo": "5. Totalmente de acuerdo",
                }

                # Contar las respuestas
                respuestas_no_reconocidas = []
                respuestas_mapeadas = 0
                
                for response in responses:
                    # ⭐ LIMPIAR LA RESPUESTA DE CARACTERES ESPECIALES Y NORMALIZAR
                    response_str = str(response).strip().lower()
                    
                    # ⭐ REEMPLAZAR CARACTERES PROBLEMÁTICOS DE CODIFICACIÓN
                    response_str = response_str.replace('▒', 'ó').replace('├í', 'í').replace('┼í', 'ó')
                    
                    print(f"Procesando respuesta: '{response_str}'")
                    
                    # Buscar coincidencia en el mapeo
                    mapped_response = response_mapping.get(response_str)
                    if mapped_response and mapped_response in response_counts:
                        response_counts[mapped_response] += 1
                        respuestas_mapeadas += 1
                        print(f"  -> Mapeada a: '{mapped_response}'")
                    else:
                        respuestas_no_reconocidas.append(response_str)
                        print(f"  -> NO RECONOCIDA: '{response_str}'")

                # Mostrar respuestas no reconocidas
                if respuestas_no_reconocidas:
                    print(f"Respuestas no reconocidas en columna {col_index}:")
                    for resp in set(respuestas_no_reconocidas):
                        print(f"  - '{resp}'")

                # Solo agregar si hay al menos una respuesta contada
                total_responses = sum(response_counts[key] for key in response_counts if key != "Pregunta")
                print(f"Total respuestas mapeadas: {respuestas_mapeadas}")
                print(f"Total respuestas contadas: {total_responses}")
                print(f"Distribucion final: {dict((k, v) for k, v in response_counts.items() if k != 'Pregunta')}")
                
                if total_responses > 0:
                    survey_data.append(response_counts)
                    print(f"EXITO: Pregunta agregada exitosamente")
                else:
                    print(f"ERROR: Pregunta no agregada - no hay respuestas validas mapeadas")

            print(f"\n=== RESUMEN FINAL ===")
            print(f"Total de preguntas procesadas exitosamente: {len(survey_data)}")
            
            if not survey_data:
                print("ERROR: No se proceso ninguna pregunta exitosamente")
                return None

            return survey_data

        except Exception as e:
            print(f"ERROR CRITICO al procesar Excel: {e}")
            print(f"Tipo de error: {type(e).__name__}")
            import traceback
            print(f"Traceback completo: {traceback.format_exc()}")
            return None

    def save_survey_json(self, survey_data, survey_type):
        """
        Guarda los datos de la encuesta como archivo JSON
        """
        try:
            # Crear directorio media si no existe
            media_path = os.path.join(settings.BASE_DIR, 'media')
            os.makedirs(media_path, exist_ok=True)

            # Nombre del archivo JSON
            json_filename = f"encuesta_{survey_type}.json"
            json_filepath = os.path.join(media_path, json_filename)

            # Guardar como JSON con formato legible
            with open(json_filepath, 'w', encoding='utf-8') as json_file:
                print(json_file)
                json.dump(survey_data, json_file, ensure_ascii=False, indent=2)

            print(f"Archivo JSON guardado: {json_filepath}")
            return json_filename

        except Exception as e:
            print(f"Error al guardar JSON: {e}")
            raise e

class SurveySearchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("=" * 50)
        print("SurveySearchView.post() llamado")
        print(f"Usuario: {request.user}")
        print(f"Datos recibidos: {request.data}")
        print("=" * 50)

        try:
            query = request.data.get('query', '').strip().lower()
            survey_types = request.data.get('survey_types', [])

            print(f"Query procesado: '{query}'")
            print(f"Survey types: {survey_types}")

            if not query or len(query) < 3:
                print("ERROR: Query muy corto o vacío")
                return Response({
                    "results": [],
                    "message": "La búsqueda debe tener al menos 3 caracteres"
                }, status=status.HTTP_400_BAD_REQUEST)

            # ⭐ DICCIONARIO PARA CONSOLIDAR PREGUNTAS POR TEXTO
            consolidated_questions = {}
            media_path = os.path.join(settings.BASE_DIR, 'media')
            print(f"Ruta de media: {media_path}")

            # Buscar en cada tipo de encuesta
            for survey_type in survey_types:
                json_filename = f"encuesta_{survey_type}.json"
                json_filepath = os.path.join(media_path, json_filename)
                
                print(f"Buscando archivo: {json_filepath}")
                print(f"Archivo existe: {os.path.exists(json_filepath)}")

                if os.path.exists(json_filepath):
                    try:
                        with open(json_filepath, 'r', encoding='utf-8') as json_file:
                            survey_data = json.load(json_file)

                        print(f"Datos cargados de {survey_type}: {len(survey_data)} preguntas")

                        # Buscar preguntas que coincidan con el query
                        matches_found = 0
                        for item in survey_data:
                            question = item.get('Pregunta', '').lower()
                            if query in question:
                                matches_found += 1
                                question_text = item.get('Pregunta', '').strip()
                                
                                # ⭐ CONSOLIDAR PREGUNTAS POR TEXTO
                                if question_text not in consolidated_questions:
                                    consolidated_questions[question_text] = {
                                        'question': question_text,
                                        'actors': {},  # Cambiar a diccionario para actores
                                        'total_responses': 0
                                    }
                                
                                # Calcular total de respuestas para este actor
                                actor_total = sum(
                                    value for key, value in item.items() 
                                    if key != 'Pregunta' and isinstance(value, (int, float))
                                )
                                
                                # ⭐ AGREGAR DATOS DEL ACTOR A LA PREGUNTA CONSOLIDADA
                                consolidated_questions[question_text]['actors'][survey_type] = {
                                    'responses': {
                                        key: value for key, value in item.items() 
                                        if key != 'Pregunta'
                                    },
                                    'total_responses': actor_total
                                }
                                
                                # Actualizar total general
                                consolidated_questions[question_text]['total_responses'] += actor_total

                        print(f"Coincidencias encontradas en {survey_type}: {matches_found}")

                    except Exception as e:
                        print(f"ERROR leyendo {json_filename}: {e}")
                        continue

            # ⭐ CONVERTIR PREGUNTAS CONSOLIDAS A FORMATO DE RESPUESTA
            results = []
            for question_text, question_data in consolidated_questions.items():
                # Crear lista de etiquetas de actores
                actor_labels = [self.get_actor_label(actor) for actor in question_data['actors'].keys()]
                
                result = {
                    'id': f"consolidated_{len(results)}",
                    'question': question_text,
                    'actors': question_data['actors'],  # Datos completos de todos los actores
                    'actor_labels': actor_labels,  # Etiquetas legibles
                    'total_responses': question_data['total_responses'],
                    'actor_count': len(question_data['actors'])
                }
                results.append(result)

            # Ordenar resultados por relevancia y total de respuestas
            results.sort(key=lambda x: (
                query in x['question'].lower(),
                x['total_responses']
            ), reverse=True)

            print(f"Total de preguntas consolidadas: {len(results)}")

            response_data = {
                "results": results,
                "total_found": len(results),
                "search_query": query
            }
            
            print("Respuesta exitosa preparada")
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"ERROR CRÍTICO en survey search: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            
            return Response({
                "error": f"Error interno al buscar preguntas: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_actor_label(self, survey_type):
        """Convierte el tipo de encuesta a etiqueta legible"""
        labels = {
            'administrativos': 'Administrativos',
            'directivos': 'Directivos', 
            'docentes': 'Docentes',
            'egresados': 'Egresados',
            'empleadores': 'Empleadores',
            'estudiantes': 'Estudiantes'
        }
        return labels.get(survey_type, survey_type.title())

class GenerateChartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Validar que el usuario tenga permisos
            if request.user.tipo_user != "admin":
                return Response(
                    {"error": "No tienes permisos para generar gráficas"}, 
                    status=status.HTTP_403_FORBIDDEN
                )

            # Obtener datos de la petición
            question_data = request.data.get('question_data')
            caracteristica_id = request.data.get('caracteristica_id')
            indicator_number = request.data.get('indicator_number', 1)

            if not question_data or not caracteristica_id:
                return Response(
                    {"error": "Datos insuficientes para generar la gráfica"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Obtener la característica para obtener su número
            caracteristica = get_object_or_404(Characteristics, pk=caracteristica_id)
            caracteristica_nombre = caracteristica.nombre
            caracteristica_numero = self.extract_characteristic_number(caracteristica_nombre)

            # Generar la gráfica
            chart_filename = self.generate_horizontal_bar_chart(
                question_data, 
                caracteristica_numero, 
                indicator_number
            )

            if chart_filename:
                # ⭐ CONSTRUIR URL COMPLETA PARA ACCESO DIRECTO A LA IMAGEN
                # Obtener el dominio del request
                protocol = 'https' if request.is_secure() else 'http'
                host = request.get_host()
                chart_url = f"{protocol}://{host}/media/graphs/{chart_filename}"
                
                # También proporcionar la ruta relativa como fallback
                chart_relative_url = f"/media/graphs/{chart_filename}"
                
                # Log de la acción
                from logs.models import Logs
                Logs.objects.create(
                    usuario=request.user,
                    accion=f"GENERATE_CHART - {chart_filename}",
                )

                return Response({
                    "message": "Gráfica generada exitosamente",
                    "filename": chart_filename,
                    "chart_url": chart_url,  # URL completa
                    "chart_relative_url": chart_relative_url,  # URL relativa
                    "question": question_data.get('question', ''),
                    "actors_included": list(question_data.get('actors', {}).keys())
                }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Error al generar la gráfica"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        except Exception as e:
            print(f"Error generating chart: {e}")
            return Response(
                {"error": f"Error interno al generar la gráfica: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def extract_characteristic_number(self, nombre):
        """Extrae el número de característica del nombre"""
        try:
            import re
            match = re.search(r'C(\d+)', nombre)
            if match:
                return int(match.group(1))
            else:
                return 1
        except:
            return 1

    def generate_horizontal_bar_chart(self, question_data, caracteristica_num, indicator_num):
        """Genera una gráfica de barras horizontales individuales con múltiples actores"""
        try:
            # ⭐ CORREGIR LA RUTA - Guardar dentro de media/graphs (NO en backend_udguard/graphs)
            media_path = os.path.join(settings.BASE_DIR, 'media')
            graphs_path = os.path.join(media_path, 'graphs')
            
            # Crear directorios si no existen
            os.makedirs(media_path, exist_ok=True)
            os.makedirs(graphs_path, exist_ok=True)

            print(f"Directorio media: {media_path}")
            print(f"Directorio graphs: {graphs_path}")
            print(f"Directorio graphs existe: {os.path.exists(graphs_path)}")

            # Configurar matplotlib
            plt.switch_backend('Agg')
            plt.style.use('default')
            
            # ⭐ OBTENER DATOS DE MÚLTIPLES ACTORES
            actors_data = question_data.get('actors', {})
            question_text = question_data.get('question', '')
            
            print(f"Generando gráfica para {len(actors_data)} actores")
            print(f"Actores: {list(actors_data.keys())}")

            if not actors_data:
                print("No hay datos de actores para generar la gráfica")
                return None

            # ⭐ MAPEO DE COLORES CONSISTENTE (REORDENADO)
            color_mapping = {
                "5. Totalmente de acuerdo": "#66BB6A",      # Verde (primera)
                "4. De acuerdo": "#42A5F5",                # Azul (segunda)
                "3. En desacuerdo": "#AB47BC",             # Púrpura (tercera)
                "2. Totalmente en desacuerdo": "#EF5350",  # Rojo (cuarta)
                "1. No tengo información o conocimiento": "#FFA726"  # Naranja (quinta)
            }

            # ⭐ PREPARAR DATOS PARA GRÁFICA DE BARRAS INDIVIDUALES
            all_options = list(color_mapping.keys())  # Ya en el orden correcto
            actor_names_with_totals = []
            
            # ⭐ CREAR ETIQUETAS DE ACTORES CON TOTALES
            for actor in actors_data.keys():
                actor_label = self.get_actor_label(actor)
                total_responses = actors_data[actor]['total_responses']
                actor_names_with_totals.append(f"{actor_label} ({total_responses})")
            
            # ⭐ CALCULAR ESPACIADO PARA BARRAS INDIVIDUALES
            num_actors = len(actor_names_with_totals)
            num_options = len(all_options)
            bar_height = 0.15  # Altura de cada barra individual
            group_spacing = 0.3  # Espacio entre grupos de actores
            
            # ⭐ CREAR GRÁFICA DE BARRAS HORIZONTALES INDIVIDUALES
            fig, ax = plt.subplots(figsize=(16, max(10, num_actors * 3)))
            
            # Calcular posiciones Y para cada actor y opción
            y_positions = []
            current_y = 0
            
            for actor_idx in range(num_actors):
                actor_positions = []
                for option_idx in range(num_options):
                    actor_positions.append(current_y)
                    current_y += bar_height
                y_positions.append(actor_positions)
                current_y += group_spacing  # Espacio entre actores
            
            # ⭐ GENERAR BARRAS INDIVIDUALES
            for option_idx, option in enumerate(all_options):
                color = color_mapping[option]
                y_vals = []
                percentages = []
                
                for actor_idx, actor_key in enumerate(actors_data.keys()):
                    actor_responses = actors_data[actor_key]['responses']
                    actor_total = actors_data[actor_key]['total_responses']
                    
                    count = actor_responses.get(option, 0)
                    percentage = (count / actor_total * 100) if actor_total > 0 else 0
                    
                    y_vals.append(y_positions[actor_idx][option_idx])
                    percentages.append(percentage)
                
                # Crear barras horizontales para esta opción
                bars = ax.barh(y_vals, percentages, height=bar_height, 
                             color=color, alpha=0.8, label=option, 
                             edgecolor='white', linewidth=1)
                
                # ⭐ AGREGAR ETIQUETAS DE PORCENTAJE EN CADA BARRA
                for bar, percentage in zip(bars, percentages):
                    if percentage > 0:  # Solo mostrar si hay datos
                        width = bar.get_width()
                        # Posicionar texto al final de la barra si hay espacio, sino dentro
                        text_x = width + 1 if width < 85 else width / 2
                        text_color = 'black' if width < 85 else 'white'
                        
                        ax.text(text_x, bar.get_y() + bar.get_height()/2, 
                               f'{percentage:.1f}%', 
                               ha='left' if width < 85 else 'center', 
                               va='center', fontweight='bold', fontsize=9, 
                               color=text_color)

            # ⭐ CONFIGURAR ETIQUETAS DEL EJE Y
            # Crear etiquetas para cada grupo de actor
            y_labels = []
            y_label_positions = []
            
            for actor_idx, actor_name in enumerate(actor_names_with_totals):
                # Posición central del grupo de barras para este actor
                group_center = sum(y_positions[actor_idx]) / len(y_positions[actor_idx])
                y_label_positions.append(group_center)
                y_labels.append(actor_name)
            
            ax.set_yticks(y_label_positions)
            ax.set_yticklabels(y_labels, fontsize=12, fontweight='bold')
            
            # ⭐ CONFIGURAR EL RESTO DEL GRÁFICO
            ax.set_xlabel('Porcentaje de Respuestas (%)', fontsize=14, fontweight='bold')
            ax.set_title(f'Distribución de Respuestas por Actor\n{question_text[:100]}...', 
                        fontsize=16, fontweight='bold', pad=25)
            
            # Configurar eje X
            ax.set_xlim(0, 100)
            ax.set_xticks(range(0, 101, 10))
            
            # ⭐ AGREGAR LEYENDA EN ORDEN CORRECTO
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', 
                     fontsize=11, title='Opciones de Respuesta', 
                     title_fontsize=12, frameon=True, shadow=True)
            
            # ⭐ AGREGAR LÍNEAS SEPARADORAS ENTRE ACTORES
            for actor_idx in range(num_actors - 1):
                separator_y = y_positions[actor_idx][-1] + bar_height + group_spacing/2
                ax.axhline(y=separator_y, color='lightgray', linestyle='--', alpha=0.5)
            
            # Configurar grid
            ax.grid(axis='x', alpha=0.3, linestyle='--')
            ax.set_axisbelow(True)
            
            # Invertir el eje Y para que el primer actor aparezca arriba
            ax.invert_yaxis()

            # Ajustar layout
            plt.tight_layout()
            plt.subplots_adjust(right=0.75, top=0.9, bottom=0.1)

            # ⭐ GUARDAR EL ARCHIVO EN LA RUTA CORRECTA
            filename = f"C{caracteristica_num}_I{indicator_num}.png"
            filepath = os.path.join(graphs_path, filename)
            
            print(f"Guardando gráfica en: {filepath}")
            
            plt.savefig(filepath, dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            plt.close()

            # ⭐ VERIFICAR QUE EL ARCHIVO SE GUARDÓ CORRECTAMENTE
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                print(f"Gráfica guardada exitosamente: {filepath}")
                print(f"Tamaño del archivo: {file_size} bytes")
                return filename
            else:
                print(f"Error: El archivo no se guardó en {filepath}")
                return None

        except Exception as e:
            print(f"Error al generar gráfica individual: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return None

    def get_actor_label(self, survey_type):
        """Convierte el tipo de encuesta a etiqueta legible"""
        labels = {
            'administrativos': 'Administrativos',
            'directivos': 'Directivos', 
            'docentes': 'Docentes',
            'egresados': 'Egresados',
            'empleadores': 'Empleadores',
            'estudiantes': 'Estudiantes'
        }
        return labels.get(survey_type, survey_type.title())