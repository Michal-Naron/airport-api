from rest_framework import serializers

from .models import (Airport, Route)


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"


class RouteDetailListSerializer(serializers.ModelSerializer):
    source = serializers.CharField(
        source="source.closest_big_city",
        read_only=True
    )
    destination = serializers.CharField(
        source="destination.closest_big_city",
        read_only=True
    )
    class Meta:
        model = Route
        fields = "__all__"


class RouteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"

