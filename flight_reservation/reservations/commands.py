from .state import PendingState
from .repositories import BookingRepository

class Command:  # Command interface
    def execute(self):
        raise NotImplementedError("Subclasses must implement this method.")

class CommandInvoker:   # Invoker class to execute all commands
    def __init__(self):
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def execute_all(self):
        results = []
        for command in self.commands:
            results.append(command.execute())
        return results

class BookFlight(Command):  # Command to book a flight
    def __init__(self, flight, user):
        self.flight = flight
        self.user = user

    def execute(self):
        booking = BookingRepository.create_booking(self.flight, self.user) # Create a new booking using Booking Repository
        if not isinstance(booking.state_instance, PendingState):
            booking.state_instance.transition(booking, PendingState()) # Transition to Pending state if not already in Pending state using state design pattern
        return booking

class ConfirmFlight(Command):   # Command to confirm a flight
    def __init__(self, booking):
        self.booking = booking

    def execute(self):
        self.booking.confirm_booking()  # calls the comfirm booking method from Model
        return f"Booking {self.booking.id} confirmed."

class CancelFlight(Command):    # Command to cancel a flight
    def __init__(self, booking):
        self.booking = booking

    def execute(self):
        self.booking.cancel_booking() # calls the cancel booking method from Model
        return f"Booking {self.booking.id} cancelled."