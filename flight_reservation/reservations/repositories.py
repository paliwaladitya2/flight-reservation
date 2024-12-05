from .models import Flight, Booking
from django.core.exceptions import ObjectDoesNotExist

class FlightRepository:
    """
    Repository class to handle database operations for Flight model.
    """

    @staticmethod
    def get_all_flights():
        """
        Fetch all flights from the database.
        :return: QuerySet of all Flight objects.
        """
        return Flight.objects.all()

    @staticmethod
    def get_flight_by_id(flight_id):
        """
        Fetch a flight by its ID.
        :param flight_id: ID of the flight.
        :return: Flight object if found.
        :raises ObjectDoesNotExist: If the flight is not found.
        """
        try:
            return Flight.objects.get(id=flight_id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f"Flight with id {flight_id} does not exist.")

    @staticmethod
    def create_flight(flight_number, departure, arrival, seats, fare):
        """
        Create a new flight with the given details.
        :return: Created Flight object.
        """
        return Flight.objects.create(
            flight_number=flight_number,
            departure=departure,
            arrival=arrival,
            seats=seats,
            fare=fare
        )

    @staticmethod
    def update_flight(flight, flight_number=None, departure=None, arrival=None, seats=None, fare=None):
        """
        Update an existing flight's details.
        :param flight: Flight object to update.
        :return: Updated Flight object.
        """
        if flight_number is not None:
            flight.flight_number = flight_number
        if departure is not None:
            flight.departure = departure
        if arrival is not None:
            flight.arrival = arrival
        if seats is not None:
            flight.seats = seats
        if fare is not None:
            flight.fare = fare
        flight.save()
        return flight


class BookingRepository:
    """
    Repository class to handle database operations for Booking model.
    """

    @staticmethod
    def get_bookings_by_user(user):
        """
        Fetch all bookings made by a specific user.
        :param user: User object.
        :return: QuerySet of Booking objects.
        """
        return Booking.objects.filter(user=user)

    @staticmethod
    def create_booking(flight, user):
        """
        Create a new booking for a specific flight and user.
        :param flight: Flight object to book.
        :param user: User making the booking.
        :return: Created Booking object.
        """
        return Booking.objects.create(flight=flight, user=user)

    @staticmethod
    def get_booking_by_id(booking_id):
        """
        Fetch a booking by its ID.
        :param booking_id: ID of the booking.
        :return: Booking object if found.
        :raises ObjectDoesNotExist: If the booking is not found.
        """
        try:
            return Booking.objects.get(id=booking_id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f"Booking with id {booking_id} does not exist.")