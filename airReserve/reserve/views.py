from django.shortcuts import  get_object_or_404
from django.contrib.auth import authenticate
from reserve.models import Booking, Flight
from reserve.serializers import FlightSerializer, BookingSerializer, UserLoginSerializer, UserRegisterSerializer
from reserve.serializers import FlightSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

# Create your views here.

# #  book a seat on a flight
# def book_seat(request, id):
#     flight = Flight.objects.get(id=id)

#     # check if a user has already booked a flight
#     existing_booking = Booking.objects.filter(user=request.user).first()

#     if existing_booking:
#         already_booked = True
#         messages.error(request, 'You have already booked a flight')
#     else:
#         already_booked = False

    
#     if request.method == 'POST':
#         seat_number = request.POST['seat_number']
#         if flight.available_seats > 0:
#             Booking.objects.create(user=request.user, flight=flight, seat_number=seat_number)
#             flight.available_seats -= 1
#             flight.save()
#             messages.success(request, 'Flight booked successfully')
#             return redirect('view_bookings')
#         else:
#             print('No seats found')
#     return render(request, 'book_seat.html', {'flight': flight, 'already_booked': already_booked})



# getting a book for a specific user
class BookingApiView(APIView):
    # check if the user is authenticated
    permission_classes = [IsAuthenticated]

    # get all bookings of a specific user
    def get(self, request):

        user = request.user
        print(user.id)
        # list all flight bookings for a specific user
        bookings = Booking.objects.filter(user=user)
        # bookings = Booking.objects.get(id=id)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #  booking a seat on a flight
    def post(self, request, id):
        
        # get a flight by id
        flight_id = Flight.objects.get(id=id)
        # flight_id = Flight.objects.get(id=request.data.get('flight'))
        # check if flight exists and available
        try:
            flight = Flight.objects.get(id=flight_id)
        except Flight.DoesNotExist:
            return Response({'error':'Flight not available'}, status=status.HTTP_404_NOT_FOUND)
        
        # check if user has already booked a seat
        existing_booking = Booking.objects.filter(user=request.user, flight=flight).exists()

        if existing_booking:
            return Response({'error':'You have already booked a seat on this flight'}, status=status.HTTP_403_FORBIDDEN)
        
        if flight_id.available_seats > 0:

            data = {
                'user': request.user.id,
                'flight': request.data.get('flight'),
                'seat_number': request.data.get('seat_number')
            }
            print(data)

            serializer = BookingSerializer(data=data)
            if serializer.is_valid():
                flight_id.available_seats -= 1
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class CancelBooking(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id, *args, **kwargs):
        booking = get_object_or_404(Booking, id=id)
        if booking.user:
            booking.delete()
            return Response({'message': 'Your booking is deleted successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Booking not found'}, status=status.HTTP_400_BAD_REQUEST)

    
# get all flights
class FlightView(APIView):
    def get(self, request):
        flights = Flight.objects.all()
        serializer = FlightSerializer(flights, many=True)
        return Response({'flights': serializer.data}, status=status.HTTP_200_OK)
    

# login a user
class LoginView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):

        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            username = request.data['username']
            # username = serializer.validated_data.get('username')
            print(username)
            password = request.data['password']
            # password = serializer.validated_data.get('password')
            print(password)

            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                # if User.objects.filter(username=request.data['username']).exists():
                #     user = User.objects.get(username=request.data['username'])
                token, created = Token.objects.get_or_create(user=user)
                print(created)
                response = {
                    'success':True,
                    'username': user.username,
                    'email':user.email,
                    'token':token.key
                }

                return Response(response, status=status.HTTP_200_OK,)
            response1 = {
                "detail":"User doesnot exist" 
            }
            return Response(response1, status=status.HTTP_404_NOT_FOUND,)
        return Response({'error' : 'User not found'}, status=status.HTTP_400_BAD_REQUEST,)
            # return Response({'error': 'request not completed'}, status=status.HTTP_400_BAD_REQUEST,)

# registering a new user 
class UserRegisterView(APIView):

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # token = Token.objects.get(user=User.objects.get(username=serializer.data['username']))
            # print(token.key)
            response = {
                "success": True,
                "user": serializer.data,
                # "token":  token
            }
            return Response(response, status=status.HTTP_200_OK,)
        raise ValidationError(
            serializer.errors, code=status.HTTP_406_NOT_ACCEPTABLE
        )

# logging out a user
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'success': True, 'detail':'Logged out'}, status=status.HTTP_200_OK)
    



    
