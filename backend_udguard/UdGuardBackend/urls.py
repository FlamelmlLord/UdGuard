from django.contrib import admin
from django.urls import path
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
    FactorsCreateListViewSet,
    FactorsListCreateCharacteristicsViewSet,
    CharacteristicListUpdateViewSet,
    #CharacteristicsListCreateIndicatorsViewSet, test import indicador por característica
    IndicatorCreateView,
    IndicatorUpdateView,
)
from events.views import EventsListCreateViewSet
from logs.views import LogsListViewSet

urlpatterns = [
    path("api/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/login/", CustomLoginView.as_view(), name="token_obtain_pair"),
    path("api/register/", RegisterUserViewSet.as_view(), name="user_register"),
    path("api/users/<int:num_page>", UserListViewSet.as_view(), name="user_list"),
    path(
        "api/users/forget/",
        PasswordResetRequestView.as_view(),
        name="user_forget_password",
    ),
    path("api/users/<int:user_id>/", UserListViewSet.as_view(), name="user_delete"),
    path(
        "api/users/forget-reset-confirm/",
        PasswordResetConfirmView.as_view(),
        name="user_reset_confirm",
    ),
    path(
        "api/auth/users/token/",
        UserByIdView.as_view(),
        name="user_get",
    ),
    path(
        "api/auth/users/<int:user_id>/",
        UserByIdView.as_view(),
        name="user_get",
    ),
    path(
        "api/events/<int:num_page>",
        EventsListCreateViewSet.as_view(),
        name="list_events",
    ),
    path(
        "api/factors/",
        FactorsCreateListViewSet.as_view(),
        name="factors",
    ),
    path(
        "api/factors/<uuid:factors_id>/characteristics/",
        FactorsListCreateCharacteristicsViewSet.as_view(),
        name="characteristics_by_factor",
    ),
    path(
        "api/characteristics/<uuid:caracteristica_id>/",
        CharacteristicListUpdateViewSet.as_view(),
        name="get_update_characteristic",
    ),
    path(
        "api/characteristics/<uuid:caracteristica_id>/indicators/",
        IndicatorCreateView.as_view(),
        name="indicators_create",
    ),

    path(
        "api/indicators/<uuid:indicador_id>/",
        IndicatorUpdateView.as_view(),
        name="indicators_update",
    ),
    path(
        "api/logs/<int:num_page>/",
        LogsListViewSet.as_view(),
        name="logs_list",
    ),
    path("admin/", admin.site.urls),
]
