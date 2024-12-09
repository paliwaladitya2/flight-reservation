from django.contrib import admin
from django.urls import path, include
from reservations import views  # Import views for serving templates

urlpatterns = [
    # Admin site
    path("admin/", admin.site.urls),

    # Public Pages
    path("", views.home_view, name="home"),  # Home page
    path("login/", views.login_view, name="login"),  # Login page
    path("logout/", views.logout_view, name="logout"),  # Logout functionality

    # Bookings Pages
    path("my-bookings/", views.my_bookings_view, name="my_bookings"),  # My Bookings page
    path("book-flight/", views.book_flight, name="book_flight"),  # Book flight page
    path("cancel-booking/", views.cancel_booking, name="cancel_booking"), 
    path("make-payment/", views.make_payment, name="make_payment"),
    path("payment-cancel/", views.payment_cancel, name="payment_cancel"),
    path("payment-success/", views.payment_success, name="payment_success"),

    # App-specific URLs
    path("reservations/", include("reservations.urls")),  # Include app routes
]