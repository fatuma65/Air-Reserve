from django.urls import path
from .views import BookingApiView, LoginView, FlightView, UserLogoutView, UserRegisterView, CancelBooking,  AdminFlightsView, ListBookingView

urlpatterns = [
    path('bookings/', ListBookingView.as_view(), name='get_bookings'),
    path('create/booking/<int:id>/', BookingApiView.as_view(), name='book_flights'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/register/', UserRegisterView.as_view(), name='register'),
    path('auth/logout/', UserLogoutView.as_view(), name='logout'),
    path('flights/', FlightView.as_view(), name='flights'),
    path('cancel/<int:id>/', CancelBooking.as_view(), name='cancel_booking'),
    path('create/flights/', AdminFlightsView.as_view(), name='create_flights')
]
