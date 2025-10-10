from django.urls import path, include
from rest_framework import routers

from .views import (
    AirportViewSet,
    RouteViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    CrewViewSet,
    FlightViewSet
)

router = routers.DefaultRouter()
router.register("airports",AirportViewSet)
router.register("routes",RouteViewSet)
router.register("airplanes-types",AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("crew", CrewViewSet)
router.register("flight", FlightViewSet)
urlpatterns = [
    path("flights/", include(router.urls))
]


app_name = "flights"