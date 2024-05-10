from django.urls import path
from . import views
from .views import BookingApiView, LoginView, FlightView, UserLogoutView, UserRegisterView, CancelBooking,  AdminFlightsView

urlpatterns = [
    path('bookings/', BookingApiView.as_view(), name='bookings'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/register/', UserRegisterView.as_view(), name='register'),
    path('auth/logout/', UserLogoutView.as_view(), name='logout'),
    path('flights/', FlightView.as_view(), name='flights'),
    path('cancel/<int:id>/', CancelBooking.as_view(), name='cancel_booking'),
    path('create/flights/', AdminFlightsView.as_view(), name='create_flights')
]
