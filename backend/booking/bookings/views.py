# bookings/views.py
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated  # ← ИСПРАВЛЕНО
from django.contrib.auth.models import User
from .models import Hotel, Booking  
from .serializers import HotelSerializer, BookingSerializer


# === РЕГИСТРАЦИЯ ===
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"error": "username и password обязательны"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Пользователь с таким именем уже существует"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return Response(
            {"message": "Пользователь успешно создан", "username": user.username},
            status=status.HTTP_201_CREATED
        )


# === КАТАЛОГ ОТЕЛЕЙ ===
class HotelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hotel.objects.all().prefetch_related('room_types')
    serializer_class = HotelSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        city = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(city__icontains=city)
        return queryset


# === БРОНИРОВАНИЕ ===
class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]  # ← теперь работает

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related('room_type__hotel')
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)