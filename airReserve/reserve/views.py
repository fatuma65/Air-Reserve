from django.shortcuts import  get_object_or_404
from django.contrib.auth import authenticate
from reserve.models import Booking, Flight
from reserve.serializers import FlightSerializer, BookingSerializer, UserLoginSerializer, UserRegisterSerializer
from reserve.serializers import FlightSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

# Create your views here.
class BookingApiView(APIView):
    # check if the user is authenticated

    # get all bookings of a specific user
    def get(self, request):
        user = request.user
        print(user.id)

        # list all flight bookings for a specific user
        bookings = Booking.objects.filter(user=user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #  booking a seat on a flight
    def post(self, request):
        user_id = request.user.id

        flight_id = request.data.get('flight')
        seat_number = request.data.get('seat_number')

        try:
            flight = Flight.objects.get(id=flight_id)
        except Flight.DoesNotExist:
            return Response({'error':'flight not found'}, status=status.HTTP_404_NOT_FOUND)

        if flight.available_seats > 0:
            flight.available_seats -= 1
            flight.save()
            data = {'user':user_id, 'flight':flight_id, 'seat_number':seat_number}
            serializer = BookingSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'flight booked successfully'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class CancelBooking(APIView):

    def delete(self, request, id, *args, **kwargs):
        booking = get_object_or_404(Booking, id=id)
        if booking.user:
            booking.delete()
            return Response({'message': 'Your booking is deleted successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Booking not found'}, status=status.HTTP_400_BAD_REQUEST)

    
# get all flights
class FlightView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        flights = Flight.objects.all()
        serializer = FlightSerializer(flights, many=True)
        return Response({'flights': serializer.data}, status=status.HTTP_200_OK)
    
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

                return Response(response, status=status.HTTP_200_OK,)
      
        return Response({'error' : 'User not found'}, status=status.HTTP_400_BAD_REQUEST,)

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
        

