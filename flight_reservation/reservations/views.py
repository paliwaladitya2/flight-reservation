from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ValidationError
from .models import Flight, Booking, CustomUser
import json
from django.views.decorators.http import require_GET
from django.contrib.sessions.models import Session

@csrf_exempt
def register_user(request):
    """
    API to register a new user.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            phone_number = data.get("phone_number")

            if not username or not password:
                return JsonResponse({"error": "Username and password are required!"}, status=400)

            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists!"}, status=400)

            user = CustomUser.objects.create_user(username=username, password=password, phone_number=phone_number)
            return JsonResponse({"message": "User registered successfully!"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid HTTP method."}, status=405)

@csrf_exempt
def login_user(request):
    """
    API to log in a user using session authentication.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)  # Creates session and sets sessionid cookie
                session_key = request.session.session_key
                print(f"Session Key: {session_key}")  # Debug the session key
                return JsonResponse({'message': 'Login successful', 'sessionid': session_key}, status=200)
            return JsonResponse({"error": "Invalid username or password."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid HTTP method."}, status=405)



@login_required
def logout_user(request):
    """
    API to log out a user.
    """
    logout(request)
    request.session.flush()
    return JsonResponse({"message": "Logout successful!"}, status=200)


@csrf_exempt  # Allow POST requests without CSRF for testing purposes (remove in production if not needed)
def get_flights(request):
    """
    API to retrieve all available flights.
    """
    if request.method == "POST":  # Changed from GET to POST
        flights = Flight.objects.all()
        flights_data = [
            {
                "id": flight.id,
                "flight_number": flight.flight_number,
                "departure": flight.departure,
                "arrival": flight.arrival,
                "seats": flight.seats,
                "fare": flight.fare,
            }
            for flight in flights
        ]
        return JsonResponse({"flights": flights_data}, status=200)
    return JsonResponse({"error": "Invalid HTTP method."}, status=405)

@csrf_exempt
@login_required  # Ensure only authenticated users can access this view
def fetch_my_bookings(request):
    if request.method == "GET":
        # Debugging to verify session
        print(f"Session ID from cookies: {request.COOKIES.get('sessionid')}")
        print(f"Authenticated User: {request.user}")
        print("this is my bookings function")

        bookings = Booking.objects.filter(user=request.user)
        bookings_data = [
            {
                "id": booking.id,
                "flight_number": booking.flight.flight_number,
                "departure": booking.flight.departure,
                "arrival": booking.flight.arrival,
                "fare": booking.flight.fare,
                "booked_at": booking.booked_at,
            }
            for booking in bookings
        ]
        return JsonResponse({"bookings": bookings_data}, status=200)
    return JsonResponse({"error": "Invalid HTTP method."}, status=405)


@csrf_exempt
@login_required
def book_flight(request):
    """
    API to book a flight.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            flight_id = data.get("flight_id")
            flight = get_object_or_404(Flight, id=flight_id)

            booking = Booking.objects.create(flight=flight, user=request.user)
            booking.confirm_booking()
            return JsonResponse({"message": "Flight booked successfully!"}, status=201)

        except ValidationError as ve:
            return JsonResponse({"error": str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid HTTP method."}, status=405)


@csrf_exempt
@login_required
def cancel_booking(request):
    """
    API to cancel a booking.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            booking_id = data.get("booking_id")
            booking = get_object_or_404(Booking, id=booking_id, user=request.user)

            booking.cancel_booking()
            return JsonResponse({"message": "Booking canceled successfully!"}, status=200)

        except ValidationError as ve:
            return JsonResponse({"error": str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid HTTP method."}, status=405)


@csrf_exempt
@staff_member_required
def add_flight(request):
    """
    API to add a new flight (Admin Only).
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            flight_number = data.get("flight_number")
            departure = data.get("departure")
            arrival = data.get("arrival")
            seats = data.get("seats")
            fare = data.get("fare")

            if not all([flight_number, departure, arrival, seats, fare]):
                return JsonResponse({"error": "All fields are required!"}, status=400)

            Flight.objects.create(
                flight_number=flight_number,
                departure=departure,
                arrival=arrival,
                seats=seats,
                fare=fare,
            )
            return JsonResponse({"message": "Flight added successfully!"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid HTTP method."}, status=405)


@csrf_exempt
@staff_member_required
def edit_flight(request, flight_id):
    """
    API to edit an existing flight (Admin Only).
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            flight = get_object_or_404(Flight, id=flight_id)

            flight.flight_number = data.get("flight_number", flight.flight_number)
            flight.departure = data.get("departure", flight.departure)
            flight.arrival = data.get("arrival", flight.arrival)
            flight.seats = data.get("seats", flight.seats)
            flight.fare = data.get("fare", flight.fare)
            flight.save()

            return JsonResponse({"message": "Flight updated successfully!"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid HTTP method."}, status=405)