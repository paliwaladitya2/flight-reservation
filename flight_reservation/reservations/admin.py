from django.contrib import admin
from .models import CustomUser, Flight, Booking
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ("flight_number", "departure", "arrival", "seats", "fare")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "flight", "booked_at")
