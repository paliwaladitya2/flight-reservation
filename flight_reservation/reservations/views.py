from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Flight, Booking, CustomUser
from django.conf import settings
import paypalrestsdk

# Public Pages
def home_view(request):
    flights = Flight.objects.all()
    return render(request, "home.html", {"flights": flights})


def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        phone_number = request.POST.get("phone_number")

        if not username or not password:
            return render(request, "register.html", {"error": "Username and password are required!"})

        if CustomUser.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already exists!"})

        CustomUser.objects.create_user(username=username, password=password, phone_number=phone_number)
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
    return render(request, "my_bookings.html", {"bookings": user_bookings})

@login_required
def cancel_booking(request):
    """
    View to cancel a booking.
    """
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        booking.cancel_booking()
        return redirect("my_bookings")
    return redirect("my_bookings")

@login_required
def book_flight(request):
    if request.method == "POST":
        flight_id = request.POST.get("flight_id")
        flight = get_object_or_404(Flight, id=flight_id)

        Booking.objects.create(flight=flight, user=request.user)
        return redirect("my_bookings")
    flights = Flight.objects.all()
    return render(request, "book_flight.html", {"flights": flights})

@login_required
def make_payment(request):
    """
    View to handle payment for a booking.
    """
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        
        # Simulate a payment process
        if booking.state == "Pending":
            booking.state = "Confirmed"
            booking.save()
            return redirect("my_bookings")
    return redirect("my_bookings")

@login_required
def checkout(request, booking_id):
    """
    View to handle the checkout process.
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        # Simulate user entering payment details (handled by PayPal)
        # Redirect to PayPal
        paypalrestsdk.configure({
            "mode": settings.PAYPAL_ENVIRONMENT,
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET,
        })

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal",
            },
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
                "amount": {
                    "total": f"{booking.flight.fare}",
                    "currency": "USD",
                },
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
    """
    Handle successful payment and update booking status.
    """
    payment_id = request.GET.get("paymentId")
    payer_id = request.GET.get("PayerID")

    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        booking_id = payment.transactions[0].item_list.items[0].sku
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        booking.state = "Confirmed"
        booking.save()
        return render(request, "payment_success.html", {"booking": booking})
    else:
        return render(request, "error.html", {"error": payment.error})