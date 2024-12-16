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

User = get_user_model() # Get the user model

class UserTests(TestCase):  # Test cases for user registration and login
    def setUp(self):    # Create a test user and client
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")

    def test_user_registration(self):   # Test user registration
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "password": "password123",
            "confirm_password": "password123",
            "email": "newuser@example.com",
        })
        self.assertEqual(response.status_code, 302)  # Redirect after registration
        self.assertTrue(User.objects.filter(username="newuser").exists())   # Check if user exists

    def test_user_login(self):  # Test user login
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "password123",
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login

class FlightTests(TestCase):    # Test cases for flight management
    def setUp(self):    # Create a test client, staff user, and flight
        self.client = Client()
        self.staff_user = User.objects.create_user(username="staff", password="password123", is_staff=True)
        self.flight = Flight.objects.create(
            flight_number="FL123",
            departure="City A",
            arrival="City B",
            seats=100,
            fare=200.00
        )

    def test_add_flight(self):  # Test adding a flight
        self.client.login(username="staff", password="password123")
        response = self.client.post(reverse("add_flight"), {
            "flight_number": "FL456",
            "departure": "City C",
            "arrival": "City D",
            "seats": 50,
            "fare": 150.00,
        })
        self.assertEqual(response.status_code, 302)  # Redirect after adding flight
        self.assertTrue(Flight.objects.filter(flight_number="FL456").exists())  # Check if flight exists

    def test_edit_flight(self): # Test editing a flight
        self.client.login(username="staff", password="password123")
        response = self.client.post(reverse("edit_flight", args=[self.flight.id]), {
            "flight_number": "FL123-UPDATED",
            "departure": "City X",
            "arrival": "City Y",
            "seats": 80,
            "fare": 250.00,
        })
        self.assertEqual(response.status_code, 302)  # Redirect after editing flight
        self.flight.refresh_from_db()   # Refresh flight from database
        self.assertEqual(self.flight.flight_number, "FL123-UPDATED")    # Check if flight is updated

class BookingTests(TestCase):   # Test cases for booking management
    def setUp(self):    # Create a test client, user, and flight
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.flight = Flight.objects.create(
            flight_number="FL123",
            departure="City A",
            arrival="City B",
            seats=100,
            fare=200.00
        )

    def test_create_booking(self):  # Test booking a flight
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("book_flight"), {"flight_id": self.flight.id})
        self.assertEqual(response.status_code, 302)  # Redirect after booking
        self.assertTrue(Booking.objects.filter(user=self.user, flight=self.flight).exists())    # Check if booking exists

    def test_confirm_booking(self): # Test confirming a booking
        booking = Booking.objects.create(user=self.user, flight=self.flight, state="PendingState")
        booking.transition(ConfirmedState())    # Confirm booking and change state
        self.assertEqual(booking.state, "ConfirmedState")   # Check if booking is confirmed

    def test_cancel_booking(self):  # Test cancelling a booking
        booking = Booking.objects.create(user=self.user, flight=self.flight, state="ConfirmedState")
        booking.transition(CancelledState())    # Cancel booking and change state
        self.assertEqual(booking.state, "CancelledState")   # Check if booking is cancelled

    def test_invalid_transition(self):  # Test invalid booking transition
        booking = Booking.objects.create(user=self.user, flight=self.flight, state="CancelledState")
        with self.assertRaises(ValueError):
            booking.transition(PendingState())  # Try to transition to pending state

class PaymentTests(TestCase):   # Test cases for payment flow
    def setUp(self):    # Create a test client, user, flight, and booking
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

    def test_payment_success(self): # Test payment success flow
        self.client.login(username="testuser", password="password123")  # Login user
        self.booking.transition(ConfirmedState())   # Confirm booking
        self.assertEqual(self.booking.state, "ConfirmedState")  # Check if booking is confirmed

class FactoryTests(TestCase):   # Test cases for flight factory
    def test_create_economy_flight(self):   # Test creating economy flight
        flight = FlightFactory.create_flight("economy")   # Create economy flight
        self.assertEqual(flight.flight_number, "E123")  # Check if flight number is correct

    def test_create_business_flight(self):  # Test creating business flight
        flight = FlightFactory.create_flight("business")    # Create business flight
        self.assertEqual(flight.flight_number, "B456")  # Check if flight number is correct

    def test_create_first_flight(self): # Test creating first class flight
        flight = FlightFactory.create_flight("first")   # Create first class flight
        self.assertEqual(flight.flight_number, "F789")  # Check if flight number is correct

    def test_invalid_flight_type(self): # Test invalid flight type
        with self.assertRaises(ValueError):  # Check if ValueError is raised
            FlightFactory.create_flight("invalid")  # Try to create flight with invalid type

class RepositoryTests(TestCase):    # Test cases for repositories
    def setUp(self):    # Create a test user and flight
        self.flight = Flight.objects.create(
            flight_number="FL123",
            departure="City A",
            arrival="City B",
            seats=100,
            fare=200.00
        )

    def test_get_flight_by_id(self):    # Test getting flight by ID
        flight = FlightRepository.get_flight_by_id(self.flight.id)  # Get flight by ID
        self.assertEqual(flight, self.flight)   # Check if fetched flight is correct

    def test_get_all_flights(self): # Test getting all flights
        flights = FlightRepository.get_all_flights()    # Get all flights
        self.assertIn(self.flight, flights) # Check if flight is in fetched flights

    def test_create_booking(self):  # Test creating a booking
        user = User.objects.create_user(username="testuser", password="password123")    # Create a test user
        booking = BookingRepository.create_booking(self.flight, user)   # Create a booking
        self.assertTrue(Booking.objects.filter(id=booking.id).exists())   # Check if booking exists

    def test_get_booking_by_id(self):   # Test getting booking by ID
        user = User.objects.create_user(username="testuser", password="password123")    # Create a test user
        booking = BookingRepository.create_booking(self.flight, user)   # Create a booking
        fetched_booking = BookingRepository.get_booking_by_id(booking.id)   # Get booking by ID
        self.assertEqual(fetched_booking, booking)  # Check if fetched booking is correct

    def test_get_nonexistent_booking(self):   # Test getting nonexistent booking
        with self.assertRaises(ObjectDoesNotExist):
            BookingRepository.get_booking_by_id(9999)   # Try to get booking with invalid ID

class CommandTests(TestCase): # Test cases for commands
    def setUp(self):    # Create a test user and flight
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.flight = Flight.objects.create(
            flight_number="FL123",
            departure="City A",
            arrival="City B",
            seats=100,
            fare=200.00
        )

    def test_book_flight_command(self): # Test booking a flight
        command = BookFlight(self.flight, self.user)    # Create book flight command
        booking = command.execute() # Execute command
        self.assertTrue(Booking.objects.filter(id=booking.id).exists())  # Check if booking exists

    def test_confirm_flight_command(self):  # Test confirming a booking
        booking = Booking.objects.create(user=self.user, flight=self.flight, state="PendingState")  # Create a pending booking
        command = ConfirmFlight(booking)    # Create confirm flight command
        result = command.execute()  # Execute command
        self.assertEqual(result, f"Booking {booking.id} confirmed.")    # Check if booking is confirmed
        booking.refresh_from_db()   # Refresh booking from database
        self.assertEqual(booking.state, "ConfirmedState")   # Check if booking state is confirmed

    def test_cancel_flight_command(self):   # Test cancelling a booking
        booking = Booking.objects.create(user=self.user, flight=self.flight, state="ConfirmedState")    # Create a confirmed booking
        command = CancelFlight(booking)   # Create cancel flight command
        result = command.execute()  # Execute command
        self.assertEqual(result, f"Booking {booking.id} cancelled.")    # Check if booking is cancelled
        booking.refresh_from_db()   # Refresh booking from database
        self.assertEqual(booking.state, "CancelledState")   # Check if booking state is cancelled