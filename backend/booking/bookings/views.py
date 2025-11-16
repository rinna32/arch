# bookings/views.py
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated  # ← ИСПРАВЛЕНО
from django.contrib.auth.models import User
from .models import Hotel, Booking, VerificationToken
from .serializers import HotelSerializer, BookingSerializer
from django.core.mail import send_mail
from django.utils.crypto import get_random_string


# === РЕГИСТРАЦИЯ ===
class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({"error": "Логин занят"}, status=400)
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email занят"}, status=400)

        user = User.objects.create_user(username, email, password)
        user.is_active = False
        user.save()

        # Генерируем токен
        token = get_random_string(32)
        VerificationToken.objects.create(user=user, token=token)

        # Ссылка
        verify_url = f"https://hotels-api-eiwu.onrender.com/api/auth/verify-email/{token}/"
        send_mail(
            'Подтвердите email',
            f'Перейдите по ссылке: {verify_url}',
            'from@example.com',
            [email],
            fail_silently=False,
        )

        return Response({"message": "Проверьте почту"}, status=201)



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