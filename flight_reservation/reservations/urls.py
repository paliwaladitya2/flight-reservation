from django.urls import path
from . import views

urlpatterns = [
    # User management
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),

    # Flight management
    #path("api/flights/", views.get_flights, name="get_flights"),
    path("admin/add-flight/", views.add_flight, name="add_flight"),
    path("admin/edit-flight/<int:flight_id>/", views.edit_flight, name="edit_flight"),

    # Booking management
    #path("my-bookings/", views.fetch_my_bookings, name="fetch_my_bookings"),
    path("book-flight/", views.book_flight, name="book_flight"),
    path("cancel-booking/", views.cancel_booking, name="cancel_booking"),
]
