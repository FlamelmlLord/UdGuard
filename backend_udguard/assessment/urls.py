# Agregar esta nueva URL al archivo de URLs
from django.urls import path
from .views import (
    FactorsCreateListViewSet,
    FactorsListCreateCharacteristicsViewSet,
    CharacteristicListUpdateViewSet,
    IndicatorCreateView,
    IndicatorUpdateView,
    SurveyUploadView,
    SurveySearchView,  # ⭐ VERIFICAR QUE ESTÉ IMPORTADA
)

urlpatterns = [
    path('factors/', FactorsCreateListViewSet.as_view(), name='factors-list-create'),
    path('factors/<uuid:factor_id>/characteristics/', FactorsListCreateCharacteristicsViewSet.as_view(), name='characteristics-list-create'),
    path('characteristics/<uuid:caracteristica_id>/', CharacteristicListUpdateViewSet.as_view(), name='characteristic-detail'),
    path('characteristics/<uuid:caracteristica_id>/indicators/', IndicatorCreateView.as_view(), name='indicators-create'),
    path('indicators/<uuid:indicator_id>/', IndicatorUpdateView.as_view(), name='indicator-update'),
    path('surveys/upload/', SurveyUploadView.as_view(), name='survey-upload'),
    # ⭐ VERIFICAR QUE ESTA RUTA ESTÉ AQUÍ
    path('surveys/search/', SurveySearchView.as_view(), name='survey-search'),
]