from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import (
    CustomLoginView,
    RegisterUserViewSet,
    UserListViewSet,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    UserByIdView,
)
from assessment.views import (
    SurveyUploadView,
    FactorsCreateListViewSet,
    FactorsListCreateCharacteristicsViewSet,
    CharacteristicListUpdateViewSet,
    IndicatorCreateView,
    IndicatorUpdateView,
)
from events.views import EventsListCreateViewSet, EventDetailViewSet, EventStatsViewSet
from logs.views import LogsListViewSet

urlpatterns = [
    path("api/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/login/", CustomLoginView.as_view(), name="token_obtain_pair"),
    path("api/register/", RegisterUserViewSet.as_view(), name="user_register"),
    
    # ⭐ RUTAS DE USUARIOS REORGANIZADAS - ORDEN ESPECÍFICO ANTES QUE GENÉRICO
    path("api/users/forget/", PasswordResetRequestView.as_view(), name="user_forget_password"),
    path("api/users/forget-reset-confirm/", PasswordResetConfirmView.as_view(), name="user_reset_confirm"),
    
    # ⭐ RUTAS CON PALABRAS CLAVE ESPECÍFICAS PRIMERO
    path("api/users/page/<int:num_page>/", UserListViewSet.as_view(), name="user_list_with_page_size"),
    
    # ⭐ RUTA PARA ACCIONES ESPECÍFICAS DEL USUARIO (DELETE, PATCH)
    path("api/users/manage/<int:user_id>/", UserListViewSet.as_view(), name="user_actions"),
    
    # ⭐ RUTA GENERAL DE USUARIOS (GET, POST)
    path("api/users/", UserListViewSet.as_view(), name="user_list_default"),
    
    path("api/auth/users/token/", UserByIdView.as_view(), name="user_get"),
    path("api/auth/users/<int:user_id>/", UserByIdView.as_view(), name="user_get_by_id"),
    
    # ⭐ RUTAS DE EVENTOS MEJORADAS
    path("api/events/", EventsListCreateViewSet.as_view(), name="events_list_create_default"),
    path("api/events/<int:num_page>/", EventsListCreateViewSet.as_view(), name="events_list_create"),
    path("api/events/stats/", EventStatsViewSet.as_view(), name="events_stats"),
    path("api/events/<uuid:event_id>/", EventDetailViewSet.as_view(), name="events_detail"),
    
    path("api/factors/", FactorsCreateListViewSet.as_view(), name="factors"),
    path("api/factors/<uuid:factors_id>/characteristics/", FactorsListCreateCharacteristicsViewSet.as_view(), name="characteristics_by_factor"),
    path("api/characteristics/<uuid:caracteristica_id>/", CharacteristicListUpdateViewSet.as_view(), name="get_update_characteristic"),
    path("api/characteristics/<uuid:caracteristica_id>/indicators/", IndicatorCreateView.as_view(), name="indicators_create"),
    path("api/indicators/<uuid:indicador_id>/", IndicatorUpdateView.as_view(), name="indicators_update"),
    
    path("api/logs/", LogsListViewSet.as_view(), name="logs_list_default"),
    path("api/logs/<int:num_page>/", LogsListViewSet.as_view(), name="logs_list"),
    
    path('admin/', admin.site.urls),
    path('api/surveys/upload/', SurveyUploadView.as_view(), name='survey-upload'),
    path('api/', include('assessment.urls')),
]

# ⭐ AGREGAR CONFIGURACIÓN PARA SERVIR ARCHIVOS MEDIA
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
