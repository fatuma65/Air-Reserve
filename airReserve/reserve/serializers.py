from rest_framework import serializers
from reserve.models import Flight, Booking
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.authentication import TokenAuthentication

class FlightSerializer(serializers.ModelSerializer):
    depature_time = serializers.DateTimeField()
    destination = serializers.CharField(max_length=200)
    available_seats = serializers.IntegerField()

    class Meta:
        model = Flight
        # fields = '__all__'
        fields = ('id', 'depature_time', 'destination', 'available_seats')


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    flight = serializers.PrimaryKeyRelatedField(queryset=Flight.objects.all())

    seat_number = serializers.IntegerField()
    
    class Meta:
        model = Booking
        fields = ('id', 'user', 'flight', 'seat_number')


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    class Meta:
        model = User
        fields = ["username", "password"]

class UserRegisterSerializer(serializers.ModelSerializer):
    authentication_classes = [TokenAuthentication]

    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username","first_name", "last_name","email", "password", "password2"]

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            detail = {
                "detail": "User Already exists!"
            }
            raise ValidationError(detail=detail)
        return username

    def validate(self, instance):
        if instance['password'] != instance['password2']:
            raise ValidationError({"message": "Password is not the same"})
        return instance
    
    def create(self, validate_data):
        password = validate_data.pop('password')
        password2 = validate_data.pop('password2')
        user = User.objects.create(**validate_data)
        user.set_password(password)
        user.save()
        return user