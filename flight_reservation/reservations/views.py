from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Flight, Booking, CustomUser
from django.conf import settings
import paypalrestsdk
from .commands import CommandInvoker,CancelFlight,BookFlight,ConfirmFlight

# Configure PayPal SDK globally
paypalrestsdk.configure({
    "mode": settings.PAYPAL_ENVIRONMENT,  # "sandbox" or "live"
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

        # Validation
        if not username or not password or not email:
            return render(request, "register.html", {"error": "All fields are required."})

        if password != confirm_password:
            return render(request, "register.html", {"error": "Passwords do not match."})

        if CustomUser.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already exists."})

        # Create the user
        CustomUser.objects.create_user(username=username, password=password, email=email)
        return redirect("login")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("my_bookings")
        return render(request, "login.html", {"error": "Invalid username or password."})
    return render(request, "login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


# Flight Management
@staff_member_required
def add_flight(request):
    if request.method == "POST":
        flight_number = request.POST.get("flight_number")
        departure = request.POST.get("departure")
        arrival = request.POST.get("arrival")
        seats = request.POST.get("seats")
        fare = request.POST.get("fare")

        Flight.objects.create(
            flight_number=flight_number,
            departure=departure,
            arrival=arrival,
            seats=seats,
            fare=fare,
        )
        return redirect("home")
    return render(request, "add_flight.html")


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
        return redirect("home")

    return render(request, "edit_flight.html", {"flight": flight})


# Booking Management
@login_required
def my_bookings_view(request):
    user_bookings = Booking.objects.filter(user=request.user)
    return render(request, "my_bookings.html", {
        "bookings": user_bookings,
        "loyalty_points": request.user.loyalty_points,
    })


@login_required
def cancel_booking(request):
    """
    View to cancel a booking.
    """
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        try:
            invoker = CommandInvoker()
            command = CancelFlight(booking)
            invoker.add_command(command)
            invoker.execute_all()
            return redirect("my_bookings")
        except Exception as e:
            return render(request, "error.html", {"error": str(e)})


@login_required
def book_flight(request):
    if request.method == "POST":
        flight_id = request.POST.get("flight_id")
        flight = get_object_or_404(Flight, id=flight_id)
        try:
            invoker = CommandInvoker()
            command = BookFlight(flight, request.user)
            invoker.add_command(command)
            invoker.execute_all()
            return redirect("my_bookings")
        except Exception as e:
            print(e)
            return render(request, "error.html", {"error": str(e)})
    flights = Flight.objects.all()
    return render(request, "home.html", {"flights": flights})



@login_required
def checkout(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": request.build_absolute_uri("/payment-success/"),
                "cancel_url": request.build_absolute_uri("/payment-cancel/"),
            },
            "transactions": [{
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

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    return redirect(link.href)
        else:
            return render(request, "error.html", {"error": payment.error})

    return render(request, "checkout.html", {"booking": booking})


@login_required
def payment_success(request):
    payment_id = request.GET.get("paymentId")
    payer_id = request.GET.get("PayerID")

    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        booking_id = payment.transactions[0].item_list.items[0].sku
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        try:
            invoker = CommandInvoker()
            command = ConfirmFlight(booking)
            invoker.add_command(command)
            invoker.execute_all()
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