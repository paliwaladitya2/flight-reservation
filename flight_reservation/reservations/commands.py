class Command:
    """
    Abstract base class for all commands.
    """

    def execute(self):
        raise NotImplementedError("Subclasses must implement this method.")


class CommandInvoker:
    """
    Invoker class to manage and execute commands.
    """

    def __init__(self):
        self.commands = []

    def add_command(self, command):
        """
        Add a command to the invoker.
        :param command: Command object to be added.
        """
        self.commands.append(command)

    def execute_all(self):
        """
        Execute all added commands.
        :return: List of results from each command's execution.
        """
        results = []
        for command in self.commands:
            results.append(command.execute())
        return results


class BookFlight(Command):
    """
    Command class to handle flight bookings.
    """

    def __init__(self, flight, user):
        """
        Initialize with the flight to book and the user.
        :param flight: Flight object.
        :param user: User object.
        """
        self.flight = flight
        self.user = user

    def execute(self):
        """
        Execute the booking command by creating a booking.
        :return: The created Booking object.
        """
        from .repositories import BookingRepository
        return BookingRepository.create_booking(self.flight, self.user)


class CancelFlight(Command):
    """
    Command class to handle booking cancellations.
    """

    def __init__(self, booking):
        """
        Initialize with the booking to cancel.
        :param booking: Booking object.
        """
        self.booking = booking

    def execute(self):
        """
        Execute the cancel command by changing the booking's state.
        :return: Success message after cancellation.
        """
        from .models import Booking
        self.booking.set_state("Cancelled")
        return f"Booking for flight {self.booking.flight.flight_number} has been cancelled successfully!"