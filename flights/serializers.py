from rest_framework import serializers

from .models import (
    Airport,
    Route,
    AirplaneType,
    Airplane
)


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


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = "__all__"


class AirplaneListSerializer(serializers.ModelSerializer):
    airplane_type = serializers.CharField(source="airplane_type.name")
    class Meta:
        model = Airplane
        fields = "__all__"


class AirplaneDetailSerializer(serializers.ModelSerializer):
    number_of_seats = serializers.IntegerField()
    airplane_type = serializers.CharField(source="airplane_type.name")
    class Meta:
        model = Airplane
        fields =  ("id","name","rows","seats_in_row","airplane_type"  ,"number_of_seats",)


class AirplaneCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = "__all__"
