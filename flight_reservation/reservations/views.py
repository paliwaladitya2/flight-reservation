from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Flight, Booking, CustomUser
from .factories import FlightFactory
from .commands import BookFlight, CancelFlight

def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        phone_number = request.POST.get("phone_number")

        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({"message": "Username already exists!"}, status=400)

        user = CustomUser.objects.create_user(
            username=username, password=password, phone_number=phone_number
        )
        return JsonResponse({"message": f"User {user.username} registered successfully!"})


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"message": f"User {user.username} logged in successfully!"})
        return JsonResponse({"message": "Invalid credentials!"}, status=401)


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related("flight")
    data = [
        {
            "flight_number": b.flight.flight_number,
            "departure": b.flight.departure,
            "arrival": b.flight.arrival,
            "fare": b.flight.fare,
            "booked_at": b.booked_at,
        }
        for b in bookings
    ]
    return JsonResponse({"my_bookings": data})


@staff_member_required
def add_flight(request):
    if request.method == "POST":
        flight = Flight.objects.create(
            flight_number=request.POST.get("flight_number"),
            departure=request.POST.get("departure"),
            arrival=request.POST.get("arrival"),
            seats=request.POST.get("seats"),
            fare=request.POST.get("fare"),
        )
        return JsonResponse({"message": f"Flight {flight.flight_number} added successfully!"})


@staff_member_required
def edit_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == "POST":
        flight.flight_number = request.POST.get("flight_number", flight.flight_number)
        flight.departure = request.POST.get("departure", flight.departure)
        flight.arrival = request.POST.get("arrival", flight.arrival)
        flight.seats = request.POST.get("seats", flight.seats)
        flight.fare = request.POST.get("fare", flight.fare)
        flight.save()
        return JsonResponse({"message": f"Flight {flight.flight_number} updated successfully!"})