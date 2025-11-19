# bookings/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from datetime import timedelta

from .models import Hotel, RoomType, Booking, VerificationToken
from .serializers import (
    HotelSerializer,
    RoomTypeSerializer,
    BookingSerializer,
    UserRegisterSerializer
)


# === РЕГИСТРАЦИЯ ===
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.is_active = False
        user.save()

        # Создаём токен подтверждения
        token = get_random_string(64)
        VerificationToken.objects.update_or_create(
            user=user,
            defaults={'token': token}
        )

        verify_url = f"http://127.0.0.1:8000/api/auth/verify-email/{token}/"

        send_mail(
            subject="Подтверждение email — Бронирование отелей",
            message=f"Привет, {user.username}!\n\n"
                    f"Перейдите по ссылке, чтобы активировать аккаунт:\n{verify_url}\n\n"
                    f"Ссылка действует 24 часа.",
            from_email="no-reply@booking.local",
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response({"message": "Проверьте почту для подтверждения email"}, status=201)

    return Response(serializer.errors, status=400)


# === ПОДТВЕРЖДЕНИЕ EMAIL ===
@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email_view(request, token):
    try:
        token_obj = VerificationToken.objects.get(token=token)
        if timezone.now() > token_obj.created_at + timedelta(hours=24):
            token_obj.delete()
            return Response({"error": "Ссылка истекла"}, status=400)

        user = token_obj.user
        user.is_active = True
        user.save()
        token_obj.delete()

        return Response({"message": "Аккаунт успешно активирован! Теперь можно войти."})

    except VerificationToken.DoesNotExist:
        return Response({"error": "Неверная или использованная ссылка"}, status=400)


# === VIEWSETЫ ===
class HotelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hotel.objects.all().prefetch_related('room_types')
    serializer_class = HotelSerializer
    permission_classes = [AllowAny]


class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer 

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related('room_type__hotel')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)