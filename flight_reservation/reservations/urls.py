from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='api_register_user'),
    path('login/', views.login_user, name='api_login_user'),
    path('my-bookings/', views.my_bookings, name='api_my_bookings'),
    path('admin/add-flight/', views.add_flight, name='api_add_flight'),
    path('admin/edit-flight/<int:flight_id>/', views.edit_flight, name='api_edit_flight'),
    path('book-flight/', views.book_flight, name='api_book_flight'),
    path('cancel-booking/', views.cancel_booking, name='api_cancel_booking'),
]
