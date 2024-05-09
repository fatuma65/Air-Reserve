from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from reserve.models import Booking, Flight
from reserve.serializers import FlightSerializer, BookingSerializer, UserLoginSerializer, UserRegisterSerializer
from reserve.serializers import FlightSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView

# Create your views here.
class BookingApiView(APIView):
    #  booking a seat on a flight
    def post(self, request, id):
        data = {}
        print(id)
        try:
            flight = Flight.objects.get(id=id)
            print(flight)
        except Flight.DoesNotExist:
            return Response({'error':'flight not found'}, status=status.HTTP_404_NOT_FOUND)

        if flight.available_seats > 0:
            flight.available_seats -= 1
            flight.save()
            data['user'] = request.user.id
            data['flight'] = flight.id
            data['seat_number'] = request.data['seat_number']
            serializer = BookingSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                print(serializer.data)
                return Response({'message':'flight booked successfully'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListBookingView(ListAPIView):
    serializer_class = BookingSerializer

    def get(self, request):
        user = request.user.id
        # list all flight bookings for a specific user
        bookings = Booking.objects.filter(user=user)
        print(bookings)
        serializer = self.get_serializer(bookings, many=True)
        print('---------bookings-----', serializer.data)
        if serializer is not None:
            return Response({'data': serializer.data, 'success': True})
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

class CancelBooking(APIView):

    def delete(self, request, id, *args, **kwargs):
        user = request.user
        print('this is the user to delete the booking',user)
        booking = Booking.objects.filter(user=user, id=id)
        print(booking)
        if booking is not None:
            booking.delete()
            return Response({'message': 'Your booking is deleted successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

    
# get all flights
class FlightView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        flights = Flight.objects.all()
        serializer = FlightSerializer(flights, many=True)
        return Response({'flights': serializer.data}, status=status.HTTP_200_OK)
    
# get a specific flight
class FlightDetailView(APIView):
    def get(self, request, id):
        flight = get_object_or_404(Flight, id=id)
        serializer = FlightSerializer(flight)
        return Response(serializer.data, status=status.HTTP_200_OK)

# login a user
class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):

        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            username = request.data['username']
            password = request.data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                response = {
                    'success':True,
                    'user_id':user.id,
                    'token':token.key
                }

                return Response(response, status=status.HTTP_200_OK)
        return Response({'error' : 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

# registering a new user 
class UserRegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "success": True,
                "user": serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK,)
        raise ValidationError(
            serializer.errors, code=status.HTTP_406_NOT_ACCEPTABLE
        )

# logging out a user
class UserLogoutView(APIView):

    def post(self, request, *args, **kwargs):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'success': True, 'detail':'Logged out'}, status=status.HTTP_200_OK)
    
# admin shuld be able to create flights
class AdminFlightsView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FlightSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"Flight successfully created"}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors})