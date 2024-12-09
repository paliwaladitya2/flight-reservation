from .state import PendingState, ConfirmedState, CancelledState

class Command:
    def execute(self):
        raise NotImplementedError("Subclasses must implement this method.")

class CommandInvoker:
    def __init__(self):  # Changed from init to __init__
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def execute_all(self):
        results = []
        for command in self.commands:
            results.append(command.execute())
        return results

class BookFlight(Command):
    def __init__(self, flight, user):  # Changed from init to __init__
        self.flight = flight
        self.user = user

    def execute(self):
        from .repositories import BookingRepository
        booking = BookingRepository.create_booking(self.flight, self.user)
        booking.transition(PendingState())
        return booking

class ConfirmFlight(Command):
    def __init__(self, booking):  # Changed from init to __init__
        self.booking = booking

    def execute(self):
        self.booking.confirm_booking()
        return f"Booking {self.booking.id} confirmed."

class CancelFlight(Command):
    def __init__(self, booking):  # Changed from init to __init__
        self.booking = booking

    def execute(self):
        self.booking.cancel_booking()
        return f"Booking {self.booking.id} cancelled."