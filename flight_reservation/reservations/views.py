from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from .repositories import FlightRepository, BookingRepository
from .commands import CommandInvoker, BookFlight
from .models import CustomUser, Flight , Booking
from .factories import FlightFactory

@csrf_exempt
def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        phone_number = request.POST.get("phone_number")

        # Validate username
        if not username:
            return JsonResponse({"message": "Username is required!"}, status=400)

        # Validate password
        if not password:
            return JsonResponse({"message": "Password is required!"}, status=400)

        # Validate uniqueness of username
        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({"message": "Username already exists!"}, status=400)

        # Create the user
        user = CustomUser.objects.create_user(
            username=username, password=password, phone_number=phone_number
        )
        return JsonResponse({"message": f"User {user.username} registered successfully!"})

    return JsonResponse({"message": "Invalid request method!"}, status=405)

@csrf_exempt
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
@csrf_exempt
def book_flight(request):
    if request.method == "POST":
        flight_id = request.POST.get("flight_id")
        flight = FlightRepository.get_flight_by_id(flight_id)

        invoker = CommandInvoker()

        booking_command = BookFlight(flight=flight, user=request.user)
        invoker.add_command(booking_command)

        results = invoker.execute_all()

        booking = results[0]  # Assuming the first command is for booking
        booking_data = {
            "id": booking.id,
            "flight_number": booking.flight.flight_number,
            "departure": booking.flight.departure,
            "arrival": booking.flight.arrival,
            "fare": booking.flight.fare,
            "booked_at": booking.booked_at,
        }

        return JsonResponse({"message": "Flight booked successfully!", "results": booking_data})


@login_required
@csrf_exempt
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
@csrf_exempt
def add_flight(request):
    if request.method == "POST":
        flight_number = request.POST.get("flight_number")
        flight_type = request.POST.get("flight_type")

        # Normal way: Create flight using explicit details
        if flight_number:
            departure = request.POST.get("departure")
            arrival = request.POST.get("arrival")
            seats = request.POST.get("seats")
            fare = request.POST.get("fare")

            # Ensure all required fields are provided
            if not all([departure, arrival, seats, fare]):
                return JsonResponse({"error": "All fields are required for custom flight creation."}, status=400)

            flight = FlightRepository.create_flight(
                flight_number=flight_number,
                departure=departure,
                arrival=arrival,
                seats=seats,
                fare=fare,
            )
            return JsonResponse({"message": f"Flight {flight.flight_number} added successfully!"})

        # Factory-based way: Create flight dynamically
        elif flight_type:
            try:
                flight = FlightFactory.create_flight(flight_type)
                return JsonResponse({"message": f"Flight {flight.flight_number} added successfully!"})
            except ValueError as e:
                return JsonResponse({"error": str(e)}, status=400)

        # Neither flight_number nor flight_type provided
        return JsonResponse({"error": "Either flight_number or flight_type must be provided."}, status=400)

@staff_member_required
@csrf_exempt
def edit_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
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
@csrf_exempt
def cancel_booking(request):
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        booking = get_object_or_404(Booking, id=booking_id)

        # Create and execute the CancelFlight command
        from .commands import CancelFlight
        cancel_command = CancelFlight(booking=booking)
        result = cancel_command.execute()

        return JsonResponse({"message": result})