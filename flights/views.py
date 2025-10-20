from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.exceptions import ValidationError
from django.db.models import F
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
    Order,
    Ticket
)
from .serializers import (
    AirportSerializer,
    RouteDetailListSerializer,
    RouteCreateSerializer,
    AirplaneTypeSerializer,
    AirplaneListSerializer,
    AirplaneDetailSerializer,
    AirplaneCreateSerializer,
    CrewSerializer,
    FlightListCreateSerializer,
    FlightDetailSerializer,
    OrderSerializer,
    OrderListAdminSerializer,
    OrderCreateSerializer,
    TicketDetailSerializer,
    TicketAdminListSerializer,
    AirplaneImageSerializer
)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all().select_related("source", "destination")
    serializer_class = RouteDetailListSerializer

    def get_serializer_class(self):

        if self.action in ("create", "update"):
            self.serializer_class = RouteCreateSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            sources = (self.request.query_params.get("source"))
            destinations = (self.request.query_params.get("destination"))

            if sources:
                sources_list = [
                    source.strip()
                    for source in sources.split(",")
                ]
                queryset = queryset.filter(
                    source__closest_big_city__in=sources_list
                )

            if destinations:
                destinations_list = [
                    destination.strip()
                    for destination in destinations.split(",")
                ]
                queryset = queryset.filter(
                    destination__closest_big_city__in=destinations_list
                )
        return queryset

    def create(self, request, *args, **kwargs):
        source = request.data.get("source")
        destination = request.data.get("destination")

        if source == destination:
            raise ValidationError(
                "Source and destination cannot be the same.")
        return super().create(request, *args, **kwargs)


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneDetailSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        elif self.action in ("create", "update"):
            return AirplaneCreateSerializer
        elif self.action == "upload_image":
            return AirplaneImageSerializer
        return AirplaneDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "retrieve":
            queryset = queryset.annotate(
                number_of_seats=F("rows") * F("seats_in_row")
            )
        return queryset

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser]
    )
    def upload_image(self, request, pk=None):
        item = self.get_object()
        serializer = self.get_serializer(item, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightListCreateSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            self.serializer_class = FlightDetailSerializer
        if self.action == "update":
            self.serializer_class = FlightListCreateSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "retrieve":
            queryset = queryset.annotate(
                number_of_seats=F("airplane__rows") * F(
                    "airplane__seats_in_row")
            )

        if self.action == "list":
            routes = self.request.query_params.get("routes")
            departures = self.request.query_params.get("departures")
            arrivals = self.request.query_params.get("arrivals")

            if routes:
                route_ids = [int(id.strip()) for id in routes.split(",") if
                             id.strip()]
                queryset = queryset.filter(route__id__in=route_ids)

            if departures:
                departure_dates = [d.strip() for d in departures.split(",") if
                                   d.strip()]
                for d in departure_dates:
                    queryset = queryset.filter(departure_time__icontains=d)

            if arrivals:
                arrival_dates = [a.strip() for a in arrivals.split(",") if
                                 a.strip()]
                for a in arrival_dates:
                    queryset = queryset.filter(arrival_time__icontains=a)

        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset =  self.queryset

        if not self.request.user.is_staff and self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user.id)

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.user.is_staff:
            serializer_class = OrderListAdminSerializer
        if self.action in ("create", "update"):
            serializer_class = OrderCreateSerializer
        return serializer_class


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketDetailSerializer
    queryset = Ticket.objects.all().select_related("order")

    def get_queryset(self):
        queryset = self.queryset
        if self.request.user.is_authenticated and not self.request.user.is_staff:
            queryset = queryset.filter(order__user__id=self.request.user.id)
        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.user.is_staff:
            serializer_class = TicketAdminListSerializer
        return serializer_class
