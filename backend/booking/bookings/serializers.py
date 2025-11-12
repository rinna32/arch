# bookings/serializers.py
from rest_framework import serializers
from .models import Hotel, RoomType, Booking


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id', 'name', 'capacity', 'price_per_night', 'available_rooms']


class HotelSerializer(serializers.ModelSerializer):
    room_types = RoomTypeSerializer(many=True, read_only=True)  # вложенные номера

    class Meta:
        model = Hotel
        fields = [
            'id', 'name', 'address', 'city', 'country',
            'description', 'rating', 'date_added', 'room_types'
        ]

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    room_type_name = serializers.CharField(source='room_type.name', read_only=True)
    hotel_name = serializers.CharField(source='room_type.hotel.name', read_only=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'room_type', 'room_type_name', 'hotel_name',
            'check_in', 'check_out', 'guests', 'total_price',
            'status', 'created_at', 'notes'
        ]
        read_only_fields = ['total_price', 'status', 'created_at', 'user']

    def validate(self, data):
        check_in = data['check_in']
        check_out = data['check_out']
        guests = data['guests']
        room_type = data['room_type']

        if check_out <= check_in:
            raise serializers.ValidationError("Дата выезда должна быть позже даты заезда.")

        if check_in < date.today():
            raise serializers.ValidationError("Дата заезда не может быть в прошлом.")

        if guests > room_type.capacity:
            raise serializers.ValidationError(
                f"Гостей ({guests}) больше, чем вместимость ({room_type.capacity})"
            )

        overlapping = Booking.objects.filter(
            room_type=room_type,
            check_out__gt=check_in,
            check_in__lt=check_out,
            status__in=['pending', 'confirmed']
        ).exists()

        if overlapping:
            raise serializers.ValidationError("Номер занят на эти даты.")

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
        """Разрешаем менять статус только на 'cancelled' и только в нужных случаях"""
        instance = self.instance  # текущая бронь
        request = self.context['request']

        # Только владелец может отменять
        if instance.user != request.user:
            raise serializers.ValidationError("Вы можете отменять только свои брони.")

        # Можно отменять только до заезда
        if instance.check_in <= date.today():
            raise serializers.ValidationError("Нельзя отменить бронь после заезда.")

        # Можно отменять только pending или confirmed
        if instance.status not in ['pending', 'confirmed']:
            raise serializers.ValidationError("Эта бронь уже отменена или завершена.")

        # Разрешаем только смену на 'cancelled'
        if value != 'cancelled':
            raise serializers.ValidationError("Можно изменить статус только на 'cancelled'.")

        return value       