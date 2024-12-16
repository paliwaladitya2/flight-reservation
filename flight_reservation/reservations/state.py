class BookingState: # abstract class for booking states
    def handle(self, booking):      # handle method
        raise NotImplementedError("Subclasses must implement this method.")

    def transition(self, booking, newstate):    # transition method
        raise NotImplementedError("Subclasses must implement this method.")


class PendingState(BookingState):  # pending state class
    def handle(self, booking): # handle method
        return "Booking is pending."

    def transition(self, booking, newstate): # transition method
        if isinstance(newstate, ConfirmedState) or isinstance(newstate, CancelledState):
            booking.state_instance = newstate
            booking.state = newstate.__class__.__name__
            booking.save()
        else:
            raise ValueError("Invalid state transition from Pending.")


class ConfirmedState(BookingState): # confirmed state class
    def handle(self, booking):  # handle method
        return "Booking is confirmed."

    def transition(self, booking, new_state):   # transition method
        if isinstance(new_state, CancelledState):
            booking.state_instance = new_state
            booking.state = new_state.__class__.__name__
            booking.save()
        else:
            raise ValueError("Invalid state transition from Confirmed.")


class CancelledState(BookingState): # cancelled state class
    def handle(self, booking): # handle method
        return "Booking is cancelled."

    def transition(self, booking, new_state): # transition method
        raise ValueError("Cannot transition from Cancelled state.")