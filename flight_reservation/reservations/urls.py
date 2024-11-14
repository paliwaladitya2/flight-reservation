from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('admin/add-flight/', views.add_flight, name='add_flight'),
    path('admin/edit-flight/<int:flight_id>/', views.edit_flight, name='edit_flight'),
]