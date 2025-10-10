from rest_framework import serializers

from .models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
    Order, Ticket
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


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "__all__"


class FlightListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = "__all__"


class FlightDetailSerializer(serializers.ModelSerializer):
    route = RouteDetailListSerializer(read_only=True)
    airplane = AirplaneListSerializer(read_only=True)
    crews = CrewSerializer(many=True)
    number_of_seats = serializers.IntegerField(read_only=True)
    class Meta:
        model = Flight
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["row", "seat", "flight", "order"]

class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = "__all__"

class OrderListAdminSerializer(serializers.ModelSerializer):
    tickets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Order
        fields = "__all__"


class OrderCreateSerializer(serializers.ModelSerializer):
    class Mate:
        model = Order
        fields = "__all__"
