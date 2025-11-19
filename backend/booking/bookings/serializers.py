# bookings/serializers.py
from datetime import date
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Hotel, RoomType, Booking


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id', 'name', 'capacity', 'price_per_night', 'available_rooms']


class HotelSerializer(serializers.ModelSerializer):
    room_types = RoomTypeSerializer(many=True, read_only=True)  

    class Meta:
        model = Hotel
        fields = [
            'id', 'name', 'address', 'city', 'country',
            'description', 'rating', 'date_added', 'room_types'
        ]

# bookings/serializers.py → BookingSerializer (ИСПРАВЛЕННЫЙ)

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    room_type_name = serializers.CharField(source='room_type.name', read_only=True)
    hotel_name = serializers.CharField(source='room_type.hotel.name', read_only=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    read_only=True

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'room_type', 'room_type_name', 'hotel_name',
            'check_in', 'check_out', 'guests', 'total_price',
            'status', 'created_at', 'notes'
        ]
        read_only_fields = ['total_price', 'status', 'created_at', 'user']

    def validate(self, data):
        from datetime import date  # ← Добавь импорт наверху файла, если нет

        check_in = data['check_in']
        check_out = data['check_out']
        guests = data['guests']
        room_type = data['room_type']

        today = date.today()

        if check_out <= check_in:
            raise serializers.ValidationError("Дата выезда должна быть позже даты заезда.")

        if check_in < today:
            raise serializers.ValidationError("Дата заезда не может быть в прошлом.")

        if guests > room_type.capacity:
            raise serializers.ValidationError(
                f"Гостей ({guests}) больше, чем вместимость номера ({room_type.capacity})"
            )

        # Проверка пересечения броней
        overlapping = Booking.objects.filter(
            room_type=room_type,
            check_out__gt=check_in,
            check_in__lt=check_out,
            status__in=['pending', 'confirmed']
        ).exclude(pk=self.instance.pk if self.instance else None).exists()

        if overlapping:
            raise serializers.ValidationError("Этот номер уже забронирован на выбранные даты.")

        return data

    def create(self, validated_data):
        nights = (validated_data['check_out'] - validated_data['check_in']).days
        total_price = validated_data['room_type'].price_per_night * nights

        booking = Booking.objects.create(
            **validated_data,
            user=self.context['request'].user,
            total_price=total_price
        )
        return booking

    def validate_status(self, value):
        """Только владелец может отменить бронь до заезда"""
        if not self.instance:
            return value

        request = self.context['request']

        if self.instance.user != request.user:
            raise serializers.ValidationError("Вы можете менять статус только своих броней.")

        if self.instance.check_in <= date.today():
            raise serializers.ValidationError("Нельзя отменить бронь в день заезда или позже.")

        if self.instance.status not in ['pending', 'confirmed']:
            raise serializers.ValidationError("Бронь уже отменена или завершена.")

        if value != 'cancelled':
            raise serializers.ValidationError("Пользователь может установить только статус 'cancelled'.")

        return value    
    
    
    
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user      