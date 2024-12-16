from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Flight, Booking, CustomUser
from .factories import FlightFactory
from django.conf import settings
import paypalrestsdk
from .commands import CommandInvoker,CancelFlight,BookFlight,ConfirmFlight

# Configuring PayPal SDK globally
paypalrestsdk.configure({
    "mode": settings.PAYPAL_ENVIRONMENT,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})

# Public Pages
def home_view(request):
    flights = Flight.objects.all()
    return render(request, "home.html", {"flights": flights})


def register(request):
    """
    View to handle user registration.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        email = request.POST.get("email")

        # Validations for various fields
        if not username or not password or not email:
            return render(request, "register.html", {"error": "All fields are required."})

        if password != confirm_password:
            return render(request, "register.html", {"error": "Passwords do not match."})

        if CustomUser.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already exists."})

        # Create the user
        CustomUser.objects.create_user(username=username, password=password, email=email)
        return redirect("login")    # Redirect to login page
    # Render the registration page
    return render(request, "register.html")


def login_view(request):    # View to handle user login
    if request.method == "POST":    # If the form is submitted
        username = request.POST.get("username")   # Get the username and password from the form
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)  # Authenticate the user
        if user:    # If the user is authenticated
            login(request, user)    # Log the user in
            return redirect("my_bookings")  # Redirect to the user's bookings page
        return render(request, "login.html", {"error": "Invalid username or password."})    # If the user is not authenticated, show an error message
    return render(request, "login.html")    # Render the login page


@login_required
def logout_view(request):   # View to handle user logout
    logout(request) # Log the user out
    return redirect("login")    # Redirect to the login page


# Flight Management
@staff_member_required
def add_flight(request):    # View to add a new flight
    if request.method == "POST":    # If the form is submitted
        flight_number = request.POST.get("flight_number")   # Get the flight details from the form
        departure = request.POST.get("departure")   
        arrival = request.POST.get("arrival")
        seats = request.POST.get("seats")
        fare = request.POST.get("fare")
        if(request.POST.get("flight_type")):    # Check if the flight type is provided
            flight_type = request.POST.get("flight_type")   # Get the flight type
            FlightFactory.create_flight(flight_type)    # Create a flight object based on the flight type using flight factory
            return redirect("home") # Redirect to the home page

        Flight.objects.create(  # Create a flight object based on the form data
            flight_number=flight_number,
            departure=departure,
            arrival=arrival,
            seats=seats,
            fare=fare,
        )
        return redirect("home") # Redirect to the home page
    return render(request, "add_flight.html")   # Render the add flight page


@staff_member_required
def edit_flight(request, flight_id):    # View to edit an existing flight
    flight = get_object_or_404(Flight, id=flight_id)    # Get the flight object based on the flight ID

    if request.method == "POST":    # If the form is submitted
        flight.flight_number = request.POST.get("flight_number", flight.flight_number)  # Update the flight details based on the form data
        flight.departure = request.POST.get("departure", flight.departure)
        flight.arrival = request.POST.get("arrival", flight.arrival)
        flight.seats = request.POST.get("seats", flight.seats)
        flight.fare = request.POST.get("fare", flight.fare)
        flight.save()
        return redirect("home") # Redirect to the home page

    return render(request, "edit_flight.html", {"flight": flight})  # Render the edit flight page


# Booking Management
@login_required
def my_bookings_view(request):  # View to display the user's bookings
    user_bookings = Booking.objects.filter(user=request.user)   # Get the bookings for the current user
    return render(request, "my_bookings.html", {    # Render the user's bookings page
        "bookings": user_bookings,
        "loyalty_points": request.user.loyalty_points,
    })


@login_required
def cancel_booking(request):
    """
    View to cancel a booking.
    """
    if request.method == "POST":    # If the form is submitted
        booking_id = request.POST.get("booking_id")  # Get the booking ID from the form
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)  # Get the booking object based on the booking ID
        try:
            invoker = CommandInvoker()  # Create a command invoker
            command = CancelFlight(booking) # Create a cancel flight command
            invoker.add_command(command)    # Add the command to the invoker
            invoker.execute_all()   # Execute the command
            return redirect("my_bookings")  # Redirect to the user's bookings page
        except Exception as e:  # Handle any exceptions
            return render(request, "error.html", {"error": str(e)})   # Render the error page with the exception message


@login_required
def book_flight(request):   # View to book a flight
    if request.method == "POST":    # If the form is submitted
        flight_id = request.POST.get("flight_id")   # Get the flight ID from the form
        flight = get_object_or_404(Flight, id=flight_id)    # Get the flight object based on the flight ID
        try:    # Try to book the flight
            invoker = CommandInvoker()  # Create a command invoker
            command = BookFlight(flight, request.user)  # Create a book flight command
            invoker.add_command(command)    # Add the command to the invoker
            invoker.execute_all()   # Execute the command
            return redirect("my_bookings")  # Redirect to the user's bookings page
        except Exception as e:  # Handle any exceptions
            print(e)
            return render(request, "error.html", {"error": str(e)})  # Render the error page with the exception message
    flights = Flight.objects.all()  # Get all flights
    return render(request, "home.html", {"flights": flights})   # Render the home page with the flights



@login_required
def checkout(request, booking_id):  # View to handle the checkout process
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)  # Get the booking object based on the booking ID

    if request.method == "POST":    # If the form is submitted
        payment = paypalrestsdk.Payment({   # Create a PayPal payment object
            "intent": "sale",   # Set the intent to sale
            "payer": {"payment_method": "paypal"},  # Set the payment method to PayPal
            "redirect_urls": {
                "return_url": request.build_absolute_uri("/payment-success/"),  # Set the return URL
                "cancel_url": request.build_absolute_uri("/payment-cancel/"),   # Set the cancel URL
            },
            "transactions": [{  # Set the transaction details
                "item_list": {
                    "items": [{
                        "name": f"Flight {booking.flight.flight_number}",
                        "sku": f"{booking.id}",
                        "price": f"{booking.flight.fare}",
                        "currency": "USD",
                        "quantity": 1,
                    }]
                },
                "amount": {"total": f"{booking.flight.fare}", "currency": "USD"},
                "description": f"Payment for booking {booking.id}.",
            }],
        })

        if payment.create():    # If the payment is created successfully
            for link in payment.links:  # Get the payment links
                if link.rel == "approval_url":  # find the approval URL
                    return redirect(link.href)  # Redirect to the approval URL
        else:
            return render(request, "error.html", {"error": payment.error})  # Render the error page with the payment error

    return render(request, "checkout.html", {"booking": booking})


@login_required
def payment_success(request):   # View to handle payment success
    payment_id = request.GET.get("paymentId")   # Get the payment ID from the returning url
    payer_id = request.GET.get("PayerID")   # Get the token from the returning url

    payment = paypalrestsdk.Payment.find(payment_id)    # Find the payment object based on the payment ID
    if payment.execute({"payer_id": payer_id}):   # Execute the payment
        booking_id = payment.transactions[0].item_list.items[0].sku # Get the booking ID from the payment object as sent in above body of checkout function
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)  # Get the booking object based on the booking ID
        try:
            invoker = CommandInvoker()  # Create a command invoker
            command = ConfirmFlight(booking)    # Create a confirm flight command
            invoker.add_command(command)    # Add the command to the invoker
            invoker.execute_all()   # Execute the command
            return render(request, "payment_success.html", {"booking": booking})
        except Exception as e:
            return render(request, "error.html", {"error": str(e)})
    else:
        return render(request, "error.html", {"error": payment.error})


@staff_member_required
def admin_dashboard(request):
    """
    View to display the admin dashboard.
    """
    bookings = Booking.objects.all()
    flights = Flight.objects.all()
    users = CustomUser.objects.all()
    return render(request, "admin_dashboard.html", {
        "bookings": bookings,
        "flights": flights,
        "users": users,
    })


@login_required
def payment_cancel(request):
    """
    Handle payment cancellation.
    """
    return render(request, "payment_cancel.html", {
        "message": "Your payment has been canceled. Please try again if you wish to proceed."
    })