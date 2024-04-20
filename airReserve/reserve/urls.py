from django.urls import path
from . import views
from .views import BookingApiView, LoginView, FlightView, UserLogoutView, UserRegisterView, CancelBooking

urlpatterns = [
    # path('book-seat/<int:id>', views.book_seat, name='book_seat'),
    # path('view-booking/', views.view_bookings, name='view_bookings'),
    # path('cancel-booking/<int:id>/', views.cancel_booking, name='cancel_booking'),
    path('api/', BookingApiView.as_view(), name='bookings'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/register/', UserRegisterView.as_view(), name='register'),
    path('api/logout/', UserLogoutView.as_view(), name='logout'),
    path('api/flights/', FlightView.as_view(), name='flights'),
    path('api/cancel/<int:id>/', CancelBooking.as_view(), name='cancel_booking'),
]
