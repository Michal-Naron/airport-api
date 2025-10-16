from django.db import models

from users.models import User


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.second_name}"


class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="routes_source")
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="routes_destination")
    distance = models.IntegerField()

    def __str__(self):
        return (f"{self.source.closest_big_city}"
                f" - {self.destination.closest_big_city}")


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType,
        on_delete=models.CASCADE,
        related_name="airplanes"
    )

    def __str__(self):
        return self.name


class Flight(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="flights"
    )
    airplane = models.ForeignKey(
        Airplane,
        on_delete=models.CASCADE,
        related_name="flights"
    )
    crews = models.ManyToManyField(Crew, related_name="flights")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f"{self.departure_time} {self.airplane}"

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders")

    def __str__(self):
        return f"{self.pk}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(
        Flight,
        related_name="tickets",
        on_delete=models.CASCADE
    )
    order = models.ForeignKey(
        Order,
        related_name="tickets",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"seat:{self.seat} ,row: {self.row}, flight: {self.flight}, order: {self.order}"

