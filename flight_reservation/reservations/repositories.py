from .models import Flight, Booking
from django.core.exceptions import ObjectDoesNotExist
from .state import PendingState
class FlightRepository: # flight repository class
    @staticmethod   
    def get_all_flights():  # get all flights from database
        return Flight.objects.all()

    @staticmethod
    def get_flight_by_id(flight_id):  # get flight by id
        try:
            return Flight.objects.get(id=flight_id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f"Flight with id {flight_id} does not exist.")

    @staticmethod
    def create_flight(flight_number, departure, arrival, seats, fare):  # create flight
        return Flight.objects.create(
            flight_number=flight_number,
            departure=departure,
            arrival=arrival,
            seats=seats,
            fare=fare
        )

    @staticmethod
    def update_flight(flight, flight_number=None, departure=None, arrival=None, seats=None, fare=None):  # update flight
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


class BookingRepository:  # booking repository class

    @staticmethod
    def get_bookings_by_user(user): # get bookings by user from database
        return Booking.objects.filter(user=user)

    @staticmethod
    def create_booking(flight, user):  # create booking
        new_object = Booking.objects.create(flight=flight, user=user)
        new_object.state_instance = PendingState()
        new_object.state = PendingState.__name__
        new_object.save()
        
        return new_object

    @staticmethod
    def get_booking_by_id(booking_id):  # get booking by id
        try:
            return Booking.objects.get(id=booking_id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f"Booking with id {booking_id} does not exist.")