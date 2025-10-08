from django.db import models

from users.models import User


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)


class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255)


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="routes_source")
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="routes_destination")
    distance = models.IntegerField(max_length=255)


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField(max_length=255)
    seats_in_row = models.IntegerField(max_length=255)
    airplane_type = models.ForeignKey(
        AirplaneType,
        on_delete=models.CASCADE,
        related_name="airplanes"
    )


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
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="Orders")


class Ticket(models.Model):
    row = models.IntegerField(max_length=255)
    seat = models.IntegerField(max_length=255)


