from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser, Flight, Booking
from .repositories import FlightRepository, BookingRepository
from .commands import BookFlight, CancelFlight, ConfirmFlight
from .state import CancelledState, ConfirmedState,PendingState

# ----------- MODEL TESTS -----------
class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="password123", phone_number="1234567890")

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
        self.flight = Flight.objects.create(flight_number="A123", departure="City A", arrival="City B", seats=100, fare=500.0)
        self.booking = Booking.objects.create(flight=self.flight, user=self.user, state="Pending")

    def test_booking_creation(self):
        self.assertEqual(self.booking.flight, self.flight)
        self.assertEqual(self.booking.user, self.user)
        self.assertEqual(self.booking.state, "Pending")

    def test_set_state(self):
        self.booking.set_state("Cancelled")
        self.assertEqual(self.booking.state, "Cancelled")
        with self.assertRaises(ValueError):
            self.booking.set_state("InvalidState")


# ----------- VIEW TESTS -----------
class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username="testuser", password="password123")
        self.flight = Flight.objects.create(flight_number="A123", departure="City A", arrival="City B", seats=100, fare=500.0)

    def test_register_user(self):
        response = self.client.post(reverse("api_register_user"), {"username": "newuser", "password": "password123"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("User newuser registered successfully!", response.json().get("message"))

    def test_login_user(self):
        response = self.client.post(reverse("api_login_user"), {"username": "testuser", "password": "password123"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("User testuser logged in successfully!", response.json().get("message"))

    def test_book_flight(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("api_book_flight"), {"flight_id": self.flight.id})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Flight booked successfully!", response.json().get("message"))


# ----------- REPOSITORY TESTS -----------
class FlightRepositoryTest(TestCase):
    def setUp(self):
        self.flight = FlightRepository.create_flight("A123", "City A", "City B", 100, 500.0)

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
        self.flight = FlightRepository.create_flight("A123", "City A", "City B", 100, 500.0)
        self.booking = BookingRepository.create_booking(self.flight, self.user)

    def test_get_bookings_by_user(self):
        bookings = BookingRepository.get_bookings_by_user(self.user)
        self.assertIn(self.booking, bookings)

    def test_get_booking_by_id(self):
        booking = BookingRepository.get_booking_by_id(self.booking.id)
        self.assertEqual(booking, self.booking)


# ----------- COMMAND TESTS -----------
class CommandPatternTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="password123")
        self.flight = FlightRepository.create_flight(
            {"flight_number": "A123", "departure": "City A", "arrival": "City B", "seats": 100, "fare": 500}
        )

    def test_book_flight_command(self):
        command = BookFlight(self.flight, self.user)
        booking = command.execute()
        self.assertEqual(booking.state, "Pending")

    def test_confirm_booking_command(self):
        booking = BookingRepository.create_booking(self.flight, self.user)
        booking.transition(PendingState())
        command = ConfirmFlight(booking)
        result = command.execute()
        self.assertEqual(booking.state, "Confirmed")

    def test_cancel_flight_command(self):
        command = CancelFlight(self.booking)
        message = command.execute()
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.state, "Cancelled")
        self.assertIn("Booking for flight", message)
# --------------STATE PATTERN TESTS--------------------
class StatePatternTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="password123")
        self.flight = FlightRepository.create_flight(
            {"flight_number": "A123", "departure": "City A", "arrival": "City B", "seats": 100, "fare": 500}
        )
        self.booking = BookingRepository.create_booking(self.flight, self.user)

    def test_booking_transitions(self):
        self.booking.transition(PendingState())
        self.assertEqual(self.booking.state, "Pending")
        self.booking.transition(ConfirmedState())
        self.assertEqual(self.booking.state, "Confirmed")
        self.booking.transition(CancelledState())
        self.assertEqual(self.booking.state, "Cancelled")