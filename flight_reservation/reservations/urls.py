from django.urls import path
from . import views

urlpatterns = [
    # Flight Management
    path("add-flight/", views.add_flight, name="add_flight"),  # Add new flight (admin only)
    path("edit-flight/<int:flight_id>/", views.edit_flight, name="edit_flight"),  # Edit existing flight

    # User Management
    path("register/", views.register, name="register"),  # User registration
    path("checkout/<int:booking_id>/", views.checkout, name="checkout"),    # Checkout page
    path("payment-success/", views.payment_success, name="payment_success") # Payment success page
]