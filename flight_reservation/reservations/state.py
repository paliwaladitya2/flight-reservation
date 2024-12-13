class BookingState:
    """
    Abstract base class for booking states.
    """
    def handle(self, booking):
        raise NotImplementedError("Subclasses must implement this method.")

    def transition(self, booking, newstate):
        raise NotImplementedError("Subclasses must implement this method.")


class PendingState(BookingState):
    """
    State representing a pending booking.
    """
    def handle(self, booking):
        return "Booking is pending."

    def transition(self, booking, newstate):
        if isinstance(newstate, ConfirmedState) or isinstance(newstate, CancelledState):
            booking.state_instance = newstate
            booking.state = newstate.__class__.__name__  # Fix here
            booking.save()
        else:
            raise ValueError("Invalid state transition from Pending.")


class ConfirmedState(BookingState):
    """
    State representing a confirmed booking.
    """
    def handle(self, booking):
        return "Booking is confirmed."

    def transition(self, booking, new_state):
        if isinstance(new_state, CancelledState):
            booking.state_instance = new_state
            booking.state = new_state.__class__.__name__  # Fix here
            booking.save()
        else:
            raise ValueError("Invalid state transition from Confirmed.")


class CancelledState(BookingState):
    """
    State representing a cancelled booking.
    """
    def handle(self, booking):
        return "Booking is cancelled."

    def transition(self, booking, new_state):
        raise ValueError("Cannot transition from Cancelled state.")