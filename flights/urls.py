from django.urls import path, include
from rest_framework import routers

from .views import (
    AirportViewSet,
    RouteViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    CrewViewSet,
    FlightViewSet,
    OrderViewSet,
    TicketViewSet
)

router = routers.DefaultRouter()
router.register("airports",AirportViewSet)
router.register("routes",RouteViewSet)
router.register("airplanes-types",AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("crews", CrewViewSet)
router.register("flights", FlightViewSet)
router.register("orders", OrderViewSet)
router.register("tickets", TicketViewSet)
urlpatterns = [
    path("flights/", include(router.urls))
]


app_name = "flights"