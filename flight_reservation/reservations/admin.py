from django.contrib import admin
from .models import CustomUser, Flight, Booking
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for the CustomUser model.
    """
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )
    list_display = ("username", "email", "phone_number", "is_staff", "is_active")
    search_fields = ("username", "email", "phone_number")
    list_filter = ("is_staff", "is_active")


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Flight model.
    """
    list_display = ("flight_number", "departure", "arrival", "seats", "fare")
    list_filter = ("departure", "arrival")
    search_fields = ("flight_number", "departure", "arrival")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Booking model.
    """
    list_display = ("user", "flight", "booked_at", "state")
    list_filter = ("state", "booked_at")
    search_fields = ("user__username", "flight__flight_number")
    date_hierarchy = "booked_at"