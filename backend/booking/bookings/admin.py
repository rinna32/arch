# bookings/admin.py
from django.contrib import admin
from .models import Hotel, RoomType, Booking

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'rating', 'room_count')
    list_filter = ('city', 'rating')
    search_fields = ('name', 'city')
    readonly_fields = ('date_added',)

    def room_count(self, obj):
        return obj.room_types.count()
    room_count.short_description = 'Номеров'

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotel', 'price_per_night', 'available_rooms')
    list_filter = ('hotel__city',)
    list_editable = ('price_per_night', 'available_rooms')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'hotel', 'check_in', 'check_out', 'total_price', 'status')
    list_filter = ('status', 'check_in', 'room_type__hotel__city')
    search_fields = ('user__username', 'room_type__hotel__name')
    readonly_fields = ('total_price', 'created_at')

    def hotel(self, obj):
        return obj.room_type.hotel.name