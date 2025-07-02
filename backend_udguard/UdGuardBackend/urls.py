from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import CustomLoginView, RegisterUserViewSet, UserListViewSet
from events.views import EventsListCreateViewSet
from assessment.views import (
    FactorsCreateListViewSet,
    FactorsListCharacteristicsViewSet,
    CharacteristicsCreateViewSet,
    CharacteristicListUpdateViewSet,
    IndicatorCreateView,
    IndicatorUpdateView,
)

urlpatterns = [
    path("api/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/login/", CustomLoginView.as_view(), name="token_obtain_pair"),
    path("api/register/", RegisterUserViewSet.as_view(), name="user_register"),
    path("api/users/", UserListViewSet.as_view(), name="user_list"),
    path("api/users/<int:user_id>/", UserListViewSet.as_view(), name="user_delete"),
    path("api/events/", EventsListCreateViewSet.as_view(), name="list_events"),
    path(
        "api/factors/",
        FactorsCreateListViewSet.as_view(),
        name="factors",
    ),
    path(
        "api/factors/<uuid:factors_id>/characteristics/",
        FactorsListCharacteristicsViewSet.as_view(),
        name="characteristics_by_factor",
    ),
    path(
        "api/factors/<uuid:factors_id>/characteristics/",
        CharacteristicsCreateViewSet.as_view(),
        name="create_characteristic",
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
    path("admin/", admin.site.urls),
]
