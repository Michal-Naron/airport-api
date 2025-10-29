from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from flights.models import Airport, Route, AirplaneType, Airplane, Crew, Flight, Order, Ticket

User = get_user_model()

class AnonymousUserAccessTests(APITestCase):
    def setUp(self):
        self.airport = Airport.objects.create(name="Test Airport", closest_big_city="CityA")
        self.airport2 = Airport.objects.create(name="Test Airport2", closest_big_city="CityB")
        self.route = Route.objects.create(source=self.airport, destination=self.airport2, distance=1000)
        self.airplane_type = AirplaneType.objects.create(name="Boeing 747")
        self.airplane = Airplane.objects.create(name="Plane1", rows=10, seats_in_row=6, airplane_type=self.airplane_type)
        self.crew = Crew.objects.create(first_name="John", second_name="Doe")
        self.flight = Flight.objects.create(route=self.route, airplane=self.airplane,
                                            departure_time="2025-10-21T10:00:00Z",
                                            arrival_time="2025-10-21T14:00:00Z")
        self.flight.crews.add(self.crew)
        self.order = Order.objects.create(user=User.objects.create_user(username="user1", password="pass1234"))
        self.ticket = Ticket.objects.create(row=1, seat=1, flight=self.flight, order=self.order)

        self.urls = {
            "airports": reverse("flights:airport-list"),
            "routes": reverse("flights:route-list"),
            "airplanes_types": reverse("flights:airplanetype-list"),
            "airplanes": reverse("flights:airplane-list"),
            "crews": reverse("flights:crew-list"),
            "flights": reverse("flights:flight-list"),
            "orders": reverse("flights:order-list"),
            "tickets": reverse("flights:ticket-list"),
        }

    def test_anonymous_user_get_list_denied(self):
        for name, url in self.urls.items():
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, f"Anonymous GET failed for {name}")

    def test_anonymous_user_post_denied(self):
        for name, url in self.urls.items():
            response = self.client.post(url, {})
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, f"Anonymous POST failed for {name}")


class AuthenticatedUserAccessTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="pass1234")
        self.client.force_authenticate(user=self.user)

        self.airport = Airport.objects.create(name="Test Airport", closest_big_city="CityA")
        self.airport2 = Airport.objects.create(name="Test Airport2", closest_big_city="CityB")
        self.route = Route.objects.create(source=self.airport, destination=self.airport2, distance=1000)
        self.airplane_type = AirplaneType.objects.create(name="Boeing 747")
        self.airplane = Airplane.objects.create(name="Plane1", rows=10, seats_in_row=6, airplane_type=self.airplane_type)
        self.crew = Crew.objects.create(first_name="John", second_name="Doe")
        self.flight = Flight.objects.create(route=self.route, airplane=self.airplane,
                                            departure_time="2025-10-21T10:00:00Z",
                                            arrival_time="2025-10-21T14:00:00Z")
        self.flight.crews.add(self.crew)

        self.urls = {
            "airports": reverse("flights:airport-list"),
            "routes": reverse("flights:route-list"),
            "airplanes_types": reverse("flights:airplanetype-list"),
            "airplanes": reverse("flights:airplane-list"),
            "crews": reverse("flights:crew-list"),
            "flights": reverse("flights:flight-list"),
            "orders": reverse("flights:order-list"),
            "tickets": reverse("flights:ticket-list"),
        }

    def test_user_is_authenticated(self):
        response = self.client.get(self.urls["flights"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_view_all(self):
        for name, url in self.urls.items():
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK, f"Authenticated GET failed for {name}")

    def test_authenticated_user_can_create_order_and_ticket_only(self):

        order_data = {"user": self.user.id}
        response = self.client.post(self.urls["orders"], order_data)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])

        ticket_data = {"row": 1, "seat": 1, "flight": self.flight.id, "order": response.data["id"]}
        response2 = self.client.post(self.urls["tickets"], ticket_data)
        self.assertIn(response2.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])

        for key in ["airports","routes","airplanes_types","airplanes","crews","flights"]:
            response = self.client.post(self.urls[key], {})
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, f"User should not POST {key}")


class AdminUserAccessTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin1234"
        )
        self.client.force_authenticate(user=self.admin)

        self.airport_a = Airport.objects.create(name="Airport A", closest_big_city="City A")
        self.airport_b = Airport.objects.create(name="Airport B", closest_big_city="City B")
        self.route = Route.objects.create(source=self.airport_a, destination=self.airport_b, distance=1200)
        self.airplane_type = AirplaneType.objects.create(name="Boeing 737")
        self.airplane = Airplane.objects.create(
            name="Plane 1", rows=20, seats_in_row=6, airplane_type=self.airplane_type
        )
        self.crew = Crew.objects.create(first_name="John", second_name="Smith")
        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time="2025-10-21T10:00:00Z",
            arrival_time="2025-10-21T12:00:00Z"
        )
        self.flight.crews.add(self.crew)
        self.order = Order.objects.create(user=self.admin)
        self.ticket = Ticket.objects.create(row=1, seat=1, flight=self.flight, order=self.order)

        self.urls = {
            "airports": reverse("flights:airport-list"),
            "routes": reverse("flights:route-list"),
            "airplanes_types": reverse("flights:airplanetype-list"),
            "airplanes": reverse("flights:airplane-list"),
            "crews": reverse("flights:crew-list"),
            "flights": reverse("flights:flight-list"),
            "orders": reverse("flights:order-list"),
            "tickets": reverse("flights:ticket-list"),
        }

    def test_admin_can_list_all_resources(self):
        for name, url in self.urls.items():
            with self.subTest(resource=name):
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code, status.HTTP_200_OK,
                    f"Admin should access GET {name}"
                )

    def test_admin_can_create_all_resources(self):
        payloads = {
            "airports": {"name": "New Airport", "closest_big_city": "City C"},
            "routes": {"source": self.airport_a.id, "destination": self.airport_b.id, "distance": 1500},
            "airplanes_types": {"name": "Airbus A320"},
            "airplanes": {
                "name": "Plane 2",
                "rows": 25,
                "seats_in_row": 6,
                "airplane_type": self.airplane_type.id
            },
            "crews": {"first_name": "Alice", "second_name": "Johnson"},
            "flights": {
                "route": self.route.id,
                "airplane": self.airplane.id,
                "departure_time": "2025-10-22T10:00:00Z",
                "arrival_time": "2025-10-22T12:00:00Z",
                "crews": [self.crew.id]
            },
            "orders": {"user": self.admin.id},
            "tickets": {
                "row": 2,
                "seat": 3,
                "flight": self.flight.id,
                "order": self.order.id
            },
        }
        order_of_creation = [
            "airports",
            "routes",
            "airplanes_types",
            "airplanes",
            "crews",
            "flights",
            "orders",
            "tickets",
        ]

        for name in order_of_creation:
            with self.subTest(resource=name):
                response = self.client.post(self.urls[name], payloads[name],
                                            format="json")
                self.assertIn(
                    response.status_code,
                    [status.HTTP_201_CREATED, status.HTTP_200_OK],
                    f"Admin should create {name}, got {response.status_code}"
                )
