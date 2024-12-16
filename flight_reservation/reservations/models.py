from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from .state import PendingState, ConfirmedState, CancelledState,BookingState

class CustomUser(AbstractUser): # custom user model
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    loyalty_points = models.IntegerField(default=0)
    def __str__(self):
        return self.username
    
    def update_loyalty_points(self, points):    # method to update loyalty points
        self.loyalty_points += points # Update loyalty points dynamically
        self.save()


class Flight(models.Model): # flight model
    flight_number = models.CharField(max_length=10, unique=True)
    departure = models.CharField(max_length=100)
    arrival = models.CharField(max_length=100)
    seats = models.IntegerField()
    fare = models.FloatField()

    def __str__(self):
        return f"{self.flight_number}: {self.departure} -> {self.arrival}"

    def book_seat(self, count=1):   # method to book a seat
        if self.seats < count:  # Check if there are enough seats available
            raise ValidationError("Not enough seats available.")
        self.seats -= count # Decrease available seats
        self.save()

    def cancel_seat(self, count=1): # method to cancel a seat
        self.seats += count # Increase available seats
        self.save()


class Booking(models.Model):    # booking model
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    state = models.CharField(max_length=50, default="PendingState")  # State as a string
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} for Flight {self.flight.flight_number} by {self.user.username}"

    @property   # property decorator
    def state_instance(self):   # method to get the state instance
        state_classes = {
            "PendingState": PendingState,
            "ConfirmedState": ConfirmedState,
            "CancelledState": CancelledState,
        }
        # Return the corresponding state instance or default to PendingState
        return state_classes.get(self.state, PendingState)()

    @state_instance.setter  # setter method for the state instance
    def state_instance(self, new_state_instance):   # method to set the state instance
        if not isinstance(new_state_instance, BookingState):    # check if the new state instance is a subclass of BookingState
            raise ValueError("Invalid state provided. Must be a subclass of BookingState.") # raise an error if the new state instance is not a subclass of BookingState
        self.state = new_state_instance.__class__.__name__  # set the state to the new state instance
        self.save()


    def transition(self, new_state_instance):   # method to transition to a new state
        if not isinstance(new_state_instance, BookingState):
            raise ValueError("Invalid state provided. Must be a subclass of BookingState.")
        # Delegate the transition to the current state instance
        self.state_instance.transition(self, new_state_instance)

    def confirm_booking(self):   # method to confirm the booking
        if isinstance(self.state_instance, PendingState):
            self.transition(ConfirmedState())  # Transition to ConfirmedState
            self.user.update_loyalty_points(10)  # Add loyalty points
            self.save()  # Save the state change to the database

    def cancel_booking(self):    # method to cancel the booking
        if isinstance(self.state_instance, ConfirmedState):
            self.transition(CancelledState())  # Transition to CancelledState
            self.user.update_loyalty_points(-10)  # Subtract loyalty points
            self.save()  # Save the state change to the database

