from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from .state import PendingState, ConfirmedState, CancelledState,BookingState

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    loyalty_points = models.IntegerField(default=0)
    def __str__(self):
        return self.username
    
    def update_loyalty_points(self, points):
        """
        Update loyalty points for the user.
        """
        self.loyalty_points += points
        self.save()


class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    departure = models.CharField(max_length=100)
    arrival = models.CharField(max_length=100)
    seats = models.IntegerField()
    fare = models.FloatField()

    def __str__(self):
        return f"{self.flight_number}: {self.departure} -> {self.arrival}"

    def book_seat(self, count=1):
        """
        Decrease available seats when a booking is made.
        """
        if self.seats < count:
            raise ValidationError("Not enough seats available.")
        self.seats -= count
        self.save()

    def cancel_seat(self, count=1):
        """
        Increase available seats when a booking is canceled.
        """
        self.seats += count
        self.save()


class Booking(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    state = models.CharField(max_length=50, default="PendingState")  # State as a string
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} for Flight {self.flight.flight_number} by {self.user.username}"

    @property
    def state_instance(self):
        """
        Dynamically instantiate the state class based on the `state` field.
        """
        state_classes = {
            "PendingState": PendingState,
            "ConfirmedState": ConfirmedState,
            "CancelledState": CancelledState,
        }
        # Return the corresponding state instance or default to PendingState
        return state_classes.get(self.state, PendingState)()

    def transition(self, new_state_instance):
        """
        Handle state transition for the booking.
        :param new_state_instance: Instance of the new state to transition to.
        """
        if not isinstance(new_state_instance, BookingState):
            raise ValueError("Invalid state provided. Must be a subclass of BookingState.")
        # Delegate the transition to the current state instance
        self.state_instance.transition(self, new_state_instance)

    def confirm_booking(self):
        """
        Confirm the booking if it's currently pending and update loyalty points.
        """
        if isinstance(self.state_instance, PendingState):
            self.transition(ConfirmedState())  # Transition to ConfirmedState
            self.user.update_loyalty_points(10)  # Add loyalty points
            self.save()  # Save the state change to the database

    def cancel_booking(self):
        """
        Cancel the booking if it's currently confirmed and update loyalty points.
        """
        if isinstance(self.state_instance, ConfirmedState):
            self.transition(CancelledState())  # Transition to CancelledState
            self.user.update_loyalty_points(-10)  # Subtract loyalty points
            self.save()  # Save the state change to the database

