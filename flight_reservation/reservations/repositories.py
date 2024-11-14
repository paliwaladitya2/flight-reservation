from .models import Flight, Booking

class FlightRepository:
    @staticmethod
    def get_all_flights():
        return Flight.objects.all()

    @staticmethod
    def get_flight_by_id(flight_id):
        return Flight.objects.get(id=flight_id)

    @staticmethod
    def create_flight(flight_number, departure, arrival, seats, fare):
        return Flight.objects.create(
            flight_number=flight_number,
            departure=departure,
            arrival=arrival,
            seats=seats,
            fare=fare
        )

    @staticmethod
    def update_flight(flight, flight_number, departure, arrival, seats, fare):
        flight.flight_number = flight_number
        flight.departure = departure
        flight.arrival = arrival
        flight.seats = seats
        flight.fare = fare
        flight.save()
        return flight


class BookingRepository:
    @staticmethod
    def get_bookings_by_user(user):
        return Booking.objects.filter(user=user)

    @staticmethod
    def create_booking(flight, user):
        return Booking.objects.create(flight=flight, user=user)