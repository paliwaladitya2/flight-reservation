from .models import Booking

class Command:
    def execute(self):
        raise NotImplementedError("Subclasses must implement this method.")


class BookFlight(Command):
    def __init__(self, flight, user):
        self.flight = flight
        self.user = user

    def execute(self):
        booking = Booking.objects.create(flight=self.flight, user=self.user)
        return booking


class CancelFlight(Command):
    def __init__(self, booking):
        self.booking = booking

    def execute(self):
        self.booking.delete()
        return "Booking canceled successfully"