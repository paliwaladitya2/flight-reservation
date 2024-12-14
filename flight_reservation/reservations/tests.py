from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import Flight, Booking
from .state import PendingState, ConfirmedState, CancelledState
from .repositories import FlightRepository, BookingRepository
from .commands import BookFlight, ConfirmFlight, CancelFlight
from .factories import FlightFactory
import logging

User = get_user_model()

class UserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")

    def test_user_registration(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "password": "password123",
            "confirm_password": "password123",
            "email": "newuser@example.com",
        })
        self.assertEqual(response.status_code, 302)  # Redirect after registration
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_user_login(self):
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "password123",
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login

class FlightTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(username="staff", password="password123", is_staff=True)
        self.flight = Flight.objects.create(
            flight_number="FL123",
            departure="City A",
            arrival="City B",
            seats=100,
            fare=200.00
        )

    def test_add_flight(self):
        self.client.login(username="staff", password="password123")
        response = self.client.post(reverse("add_flight"), {
            "flight_number": "FL456",
            "departure": "City C",
            "arrival": "City D",
            "seats": 50,
            "fare": 150.00,
        })
        self.assertEqual(response.status_code, 302)  # Redirect after adding flight
        self.assertTrue(Flight.objects.filter(flight_number="FL456").exists())

    def test_edit_flight(self):
        self.client.login(username="staff", password="password123")
        response = self.client.post(reverse("edit_flight", args=[self.flight.id]), {
            "flight_number": "FL123-UPDATED",
            "departure": "City X",
            "arrival": "City Y",
            "seats": 80,
            "fare": 250.00,
        })
        self.assertEqual(response.status_code, 302)  # Redirect after editing flight
        self.flight.refresh_from_db()
        self.assertEqual(self.flight.flight_number, "FL123-UPDATED")

class BookingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.flight = Flight.objects.create(
            flight_number="FL123",
            departure="City A",
            arrival="City B",
            seats=100,
            fare=200.00
        )

    def test_create_booking(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("book_flight"), {"flight_id": self.flight.id})
        self.assertEqual(response.status_code, 302)  # Redirect after booking
        self.assertTrue(Booking.objects.filter(user=self.user, flight=self.flight).exists())

    def test_confirm_booking(self):
        booking = Booking.objects.create(user=self.user, flight=self.flight, state="PendingState")
        booking.transition(ConfirmedState())
        self.assertEqual(booking.state, "ConfirmedState")

    def test_cancel_booking(self):
        booking = Booking.objects.create(user=self.user, flight=self.flight, state="ConfirmedState")
        booking.transition(CancelledState())
        self.assertEqual(booking.state, "CancelledState")

    def test_invalid_transition(self):
        booking = Booking.objects.create(user=self.user, flight=self.flight, state="CancelledState")
        with self.assertRaises(ValueError):
            booking.transition(PendingState())

class PaymentTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.flight = Flight.objects.create(
            flight_number="FL123",
            departure="City A",
            arrival="City B",
            seats=100,
            fare=200.00
        )
        self.booking = Booking.objects.create(user=self.user, flight=self.flight, state="PendingState")

    def test_payment_success(self):
        self.client.login(username="testuser", password="password123")
        # Mock payment success flow
        self.booking.transition(ConfirmedState())
        self.assertEqual(self.booking.state, "ConfirmedState")

class FactoryTests(TestCase):
    def test_create_economy_flight(self):
        flight = FlightFactory.create_flight("economy")
        self.assertEqual(flight.flight_number, "E123")

    def test_create_business_flight(self):
        flight = FlightFactory.create_flight("business")
        self.assertEqual(flight.flight_number, "B456")

    def test_create_first_flight(self):
        flight = FlightFactory.create_flight("first")
        self.assertEqual(flight.flight_number, "F789")

    def test_invalid_flight_type(self):
        with self.assertRaises(ValueError):
            FlightFactory.create_flight("invalid")

class RepositoryTests(TestCase):
    def setUp(self):
        self.flight = Flight.objects.create(
            flight_number="FL123",
            departure="City A",
            arrival="City B",
            seats=100,
            fare=200.00
        )

    def test_get_flight_by_id(self):
        flight = FlightRepository.get_flight_by_id(self.flight.id)
        self.assertEqual(flight, self.flight)

    def test_get_all_flights(self):
        flights = FlightRepository.get_all_flights()
        self.assertIn(self.flight, flights)

    def test_create_booking(self):
        user = User.objects.create_user(username="testuser", password="password123")
        booking = BookingRepository.create_booking(self.flight, user)
        self.assertTrue(Booking.objects.filter(id=booking.id).exists())

    def test_get_booking_by_id(self):
        user = User.objects.create_user(username="testuser", password="password123")
        booking = BookingRepository.create_booking(self.flight, user)
        fetched_booking = BookingRepository.get_booking_by_id(booking.id)
        self.assertEqual(fetched_booking, booking)

    def test_get_nonexistent_booking(self):
        with self.assertRaises(ObjectDoesNotExist):
            BookingRepository.get_booking_by_id(9999)

class CommandTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.flight = Flight.objects.create(
            flight_number="FL123",
            departure="City A",
            arrival="City B",
            seats=100,
            fare=200.00
        )

    def test_book_flight_command(self):
        command = BookFlight(self.flight, self.user)
        booking = command.execute()
        self.assertTrue(Booking.objects.filter(id=booking.id).exists())

    def test_confirm_flight_command(self):
        booking = Booking.objects.create(user=self.user, flight=self.flight, state="PendingState")
        command = ConfirmFlight(booking)
        result = command.execute()
        self.assertEqual(result, f"Booking {booking.id} confirmed.")
        booking.refresh_from_db()
        self.assertEqual(booking.state, "ConfirmedState")

    def test_cancel_flight_command(self):
        booking = Booking.objects.create(user=self.user, flight=self.flight, state="ConfirmedState")
        command = CancelFlight(booking)
        result = command.execute()
        self.assertEqual(result, f"Booking {booking.id} cancelled.")
        booking.refresh_from_db()
        self.assertEqual(booking.state, "CancelledState")