from django.contrib import admin
from django.urls import path, include
from reservations import views

urlpatterns = [
    path("admin/", admin.site.urls),  # Django admin site
    path("api/flights/", views.get_flights, name="get_flights"),
    path("api/my-bookings/", views.fetch_my_bookings, name="fetch_my_bookings"),  # API endpoint for React
    path("api/v1/reservations/", include("reservations.urls")),  # Include app routes
]
