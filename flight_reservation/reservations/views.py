from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .repositories import FlightRepository, BookingRepository
from .commands import CommandInvoker, BookFlight
from .models import CustomUser

# Register a new user
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


# Login a user
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
def book_flight(request):
    if request.method == "POST":
        flight_id = request.POST.get("flight_id")
        flight = FlightRepository.get_flight_by_id(flight_id)

        # Create an invoker to manage commands
        invoker = CommandInvoker()

        # Add the BookFlight command
        booking_command = BookFlight(flight=flight, user=request.user)
        invoker.add_command(booking_command)

        # Execute all commands
        results = invoker.execute_all()

        return JsonResponse({"message": "Flight booked successfully!", "results": results})


@login_required
def my_bookings(request):
    bookings = BookingRepository.get_bookings_by_user(request.user)
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
        flight_number = request.POST.get("flight_number")
        departure = request.POST.get("departure")
        arrival = request.POST.get("arrival")
        seats = request.POST.get("seats")
        fare = request.POST.get("fare")

        flight = FlightRepository.create_flight(
            flight_number=flight_number,
            departure=departure,
            arrival=arrival,
            seats=seats,
            fare=fare
        )
        return JsonResponse({"message": f"Flight {flight.flight_number} added successfully!"})


@staff_member_required
def edit_flight(request, flight_id):
    flight = get_object_or_404(FlightRepository.get_flight_by_id(flight_id))
    if request.method == "POST":
        flight_number = request.POST.get("flight_number", flight.flight_number)
        departure = request.POST.get("departure", flight.departure)
        arrival = request.POST.get("arrival", flight.arrival)
        seats = request.POST.get("seats", flight.seats)
        fare = request.POST.get("fare", flight.fare)

        FlightRepository.update_flight(
            flight=flight,
            flight_number=flight_number,
            departure=departure,
            arrival=arrival,
            seats=seats,
            fare=fare
        )
        return JsonResponse({"message": f"Flight {flight.flight_number} updated successfully!"})

@login_required
def cancel_booking(request):
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        booking = get_object_or_404(BookingRepository.get_booking_by_id(booking_id, request.user))

        # Create and execute the CancelFlight command
        from .commands import CancelFlight
        cancel_command = CancelFlight(booking=booking)
        result = cancel_command.execute()

        return JsonResponse({"message": result})