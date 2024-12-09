from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from .state import PendingState, ConfirmedState, CancelledState

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
    flight = models.ForeignKey("Flight", on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, related_name="bookings")
    booked_at = models.DateTimeField(auto_now_add=True)
    STATE_CHOICES = [
        ("PendingState", "Pending"),
        ("ConfirmedState", "Confirmed"),
        ("CancelledState", "Cancelled"),
    ]
    state = models.CharField(max_length=50, choices=STATE_CHOICES, default="PendingState")

    def init(self, args, **kwargs):
        super().init(args, **kwargs)
        # Initialize the state instance based on the state field
        self.state_instance = self.get_state_instance()

    def get_state_instance(self):
        """
        Return the state instance corresponding to the current state.
        """
        state_classes = {
            "PendingState": PendingState(),
            "ConfirmedState": ConfirmedState(),
            "CancelledState": CancelledState(),
        }
        return state_classes.get(self.state, PendingState())

    def handle(self):
        """
        Delegate the handle logic to the state instance.
        """
        return self.state_instance.handle(self)

    def transition(self, new_state):
        """
        Delegate the transition logic to the state instance.
        """
        self.state_instance.transition(self, new_state)

    def confirm_booking(self):
        """
        Confirm a booking and add loyalty points.
        """
        self.user.update_loyalty_points(10)  # Add 10 loyalty points
        self.transition(ConfirmedState())

    def cancel_booking(self):
        """
        Cancel a booking and deduct loyalty points.
        """
        self.user.update_loyalty_points(-10)  # Deduct 10 loyalty points
        self.transition(CancelledState())