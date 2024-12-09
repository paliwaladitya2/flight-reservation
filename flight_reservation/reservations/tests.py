from django.test import TestCase, Client
from django.urls import reverse
from .models import CustomUser, Flight, Booking
from .repositories import FlightRepository, BookingRepository
from .commands import BookFlight, CancelFlight, ConfirmFlight
from .state import CancelledState, ConfirmedState, PendingState

# ----------- MODEL TESTS -----------
class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password123", phone_number="1234567890"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.phone_number, "1234567890")
        self.assertTrue(self.user.check_password("password123"))


class FlightModelTest(TestCase):
    def setUp(self):
        self.flight = Flight.objects.create(
            flight_number="A123",
            departure="City A",
            arrival="City B",
            seats=100,
            fare=500.0,
        )

    def test_flight_creation(self):
        self.assertEqual(self.flight.flight_number, "A123")
        self.assertEqual(self.flight.departure, "City A")
        self.assertEqual(self.flight.arrival, "City B")
        self.assertEqual(self.flight.seats, 100)
        self.assertEqual(self.flight.fare, 500.0)


class BookingModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="password123")
        self.flight = Flight.objects.create(
            flight_number="A123", departure="City A", arrival="City B", seats=100, fare=500.0
        )
        self.booking = Booking.objects.create(flight=self.flight, user=self.user, state="PendingState")

    def test_booking_creation(self):
        self.assertEqual(self.booking.flight, self.flight)
        self.assertEqual(self.booking.user, self.user)
        self.assertEqual(self.booking.state, "PendingState")

    def test_confirm_booking(self):
        self.booking.confirm_booking()
        self.user.refresh_from_db()  # Reload user data from the database to get updated loyalty points
        self.assertEqual(self.booking.state, "ConfirmedState")
        self.assertEqual(self.user.loyalty_points, 10)  # Test loyalty points addition


# ----------- VIEW TESTS -----------
class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username="testuser", password="password123")
        self.flight = Flight.objects.create(
            flight_number="A123", departure="City A", arrival="City B", seats=100, fare=500.0
        )

    def test_register_user(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "password": "password123",
                "confirm_password": "password123",
                "email": "test@example.com",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(CustomUser.objects.filter(username="newuser").exists())

    def test_login_user(self):
        response = self.client.post(reverse("login"), {"username": "testuser", "password": "password123"})
        self.assertEqual(response.status_code, 302)  # Redirect to bookings
        self.assertEqual(response.url, reverse("my_bookings"))

# ----------- REPOSITORY TESTS -----------
# Assume repositories perform CRUD operations on Flight and Booking models

class FlightRepositoryTest(TestCase):
    def setUp(self):
        self.flight = FlightRepository.create_flight(
            flight_number="A123", departure="City A", arrival="City B", seats=100, fare=500.0
        )

    def test_get_all_flights(self):
        flights = FlightRepository.get_all_flights()
        self.assertIn(self.flight, flights)

    def test_get_flight_by_id(self):
        flight = FlightRepository.get_flight_by_id(self.flight.id)
        self.assertEqual(flight, self.flight)

    def test_update_flight(self):
        updated_flight = FlightRepository.update_flight(self.flight, seats=150)
        self.assertEqual(updated_flight.seats, 150)

class BookingRepositoryTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="password123")
        self.flight = FlightRepository.create_flight(
            flight_number="A123", departure="City A", arrival="City B", seats=100, fare=500.0
        )
        self.booking = BookingRepository.create_booking(self.flight, self.user)

    def test_get_bookings_by_user(self):
        bookings = BookingRepository.get_bookings_by_user(self.user)
        self.assertIn(self.booking, bookings)

    def test_get_booking_by_id(self):
        booking = BookingRepository.get_booking_by_id(self.booking.id)
        self.assertEqual(booking, self.booking)

# ----------- COMMAND TESTS -----------
# Tests for command patterns for book, confirm, and cancel flights

class CommandPatternTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="password123")
        self.flight = Flight.objects.create(
            flight_number="A123", departure="City A", arrival="City B", seats=100, fare=500.0
        )
        self.booking = Booking.objects.create(flight=self.flight, user=self.user, state="PendingState")

    def test_book_flight_command(self):
        command = BookFlight(self.flight, self.user)
        booking = command.execute()
        self.assertEqual(booking.state, "PendingState")

    def test_confirm_flight_command(self):
        command = ConfirmFlight(self.booking)
        command.execute()
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.state, "ConfirmedState")