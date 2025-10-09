from rest_framework import viewsets
from rest_framework.exceptions import ValidationError


from .models import (
    Airport,
    Route,
    AirplaneType
)
from .serializers import (
    AirportSerializer,
    RouteDetailListSerializer,
    RouteCreateSerializer,
    AirplaneTypeSerializer
)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all().select_related("source", "destination")
    serializer_class = RouteDetailListSerializer

    def get_serializer_class(self):

        if self.action == "create":
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



