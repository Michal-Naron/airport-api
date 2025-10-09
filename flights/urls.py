from django.urls import path, include
from rest_framework import routers

from .views import (AirportViewSet, RouteViewSet)

router = routers.DefaultRouter()
router.register("airports",AirportViewSet)
router.register("routes",RouteViewSet )
urlpatterns = [
    path("flights/", include(router.urls))
]


app_name = "flights"