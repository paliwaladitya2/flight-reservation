from .state import PendingState, ConfirmedState, CancelledState


class Command:
    def execute(self):
        raise NotImplementedError("Subclasses must implement this method.")


class CommandInvoker:
    def init(self):
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def execute_all(self):
        results = []
        for command in self.commands:
            results.append(command.execute())
        return results


class BookFlight(Command):
    def init(self, flight, user):
        self.flight = flight
        self.user = user

    def execute(self):
        from .repositories import BookingRepository
        booking = BookingRepository.create_booking(self.flight, self.user)
        booking.transition(PendingState())
        return booking


class ConfirmFlight(Command):
    def init(self, booking):
        self.booking = booking

    def execute(self):
        self.booking.confirm_booking()
        return f"Booking {self.booking.id} confirmed."


class CancelFlight(Command):
    def init(self, booking):
        self.booking = booking

    def execute(self):
        self.booking.cancel_booking()
        return f"Booking {self.booking.id} cancelled."