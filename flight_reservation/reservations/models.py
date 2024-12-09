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
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(auto_now_add=True)
    STATE_CHOICES = [
        ('PendingState', 'Pending'),
        ('ConfirmedState', 'Confirmed'),
        ('CancelledState', 'Cancelled'),
    ]
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='PendingState')

    def transition(self, new_state):
        if new_state in [choice[0] for choice in self.STATE_CHOICES]:
            self.state = new_state
            self.save()
            return True
        return False

    def confirm_booking(self):
        if self.state == 'PendingState':
            self.transition('ConfirmedState')
            self.user.update_loyalty_points(10)  # Ensure loyalty points are updated correctly
            self.save()

    def cancel_booking(self):
        if self.state == 'ConfirmedState':
            self.transition('CancelledState')
            self.user.update_loyalty_points(-10)  # Ensure loyalty points are updated correctly
            self.save()

    def __str__(self):
        return f'{self.user.username} booking for {self.flight.flight_number} - {self.state}'