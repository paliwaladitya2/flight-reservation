from django.contrib.auth.models import AbstractUser
from django.db import models

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


class Booking(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    STATE_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled"),
    ]
    state = models.CharField(max_length=50, choices=STATE_CHOICES, default="Pending")

    def __str__(self):
        return f"Booking by {self.user.username} for {self.flight}"
    
    def set_state(self, state):
        if state not in dict(self.STATE_CHOICES):
            raise ValueError(f"Invalid state: {state}")
        self.state = state
        self.save()
        
    def handle(self):
        state_class = globals().get(f"{self.state}State")
        if state_class:
            return state_class().handle(self)
        return "Invalid state."


class BookingState:
    def handle(self, booking):
        raise NotImplementedError("Subclasses must implement this method.")
    
class Pending(BookingState):
    def handle(self, booking):
        raise "Bookinig is pending."
    
class Confirmed(BookingState):
    def handle(self, booking):
        raise "Booking is confirmed."
    
class Cancelled(BookingState):
    def handle(self, booking):
        raise "Booking is cancelled."
