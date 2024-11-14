class Command:
    def execute(self):
        raise NotImplementedError("Subclasses must implement this method.")


class CommandInvoker:
    def __init__(self):
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def execute_all(self):
        results = []
        for command in self.commands:
            results.append(command.execute())
        return results


class BookFlight(Command):
    def __init__(self, flight, user):
        self.flight = flight
        self.user = user

    def execute(self):
        from .repositories import BookingRepository
        return BookingRepository.create_booking(self.flight, self.user)