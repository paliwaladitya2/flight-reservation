from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username


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
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="bookings")
    booked_at = models.DateTimeField(auto_now_add=True)
    STATE_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled"),
    ]
    state = models.CharField(max_length=50, choices=STATE_CHOICES, default="Pending")

    def __str__(self):
        return f"Booking: {self.flight.flight_number} by {self.user.username}"

    def confirm_booking(self):
        """
        Confirm a booking and reduce flight seats.
        """
        if self.state != "Pending":
            raise ValidationError("Booking cannot be confirmed in its current state.")
        self.flight.book_seat()
        self.state = "Confirmed"
        self.save()

    def cancel_booking(self):
        """
        Cancel a booking and release flight seats.
        """
        if self.state != "Confirmed":
            raise ValidationError("Only confirmed bookings can be canceled.")
        self.flight.cancel_seat()
        self.state = "Cancelled"
        self.save()