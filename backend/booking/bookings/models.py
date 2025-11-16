from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
import datetime


class Hotel(models.Model):
    """Отель, в котором можно забронировать номер"""
    name = models.CharField("название отеля", max_length=200)
    address = models.CharField("адрес", max_length=300, blank=True)
    city = models.CharField("город", max_length=100)
    country = models.CharField("страна", max_length=100)
    description = models.TextField("описание", blank=True)
    rating = models.PositiveSmallIntegerField("рейтинг (1-5)", default=3, validators=[MinValueValidator(1)])
    date_added = models.DateTimeField("дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = "отель"
        verbose_name_plural = "отели"
        ordering = ['name']
        unique_together = ['name', 'city', 'country']

    def __str__(self):
        return f"{self.name}, {self.city}"


class RoomType(models.Model):
    """Тип номера (например: Стандарт, Люкс, Семейный)"""
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_types')
    name = models.CharField("тип номера", max_length=100)
    capacity = models.PositiveSmallIntegerField("вместимость (чел.)")
    price_per_night = models.DecimalField("цена за ночь", max_digits=10, decimal_places=2)
    available_rooms = models.PositiveSmallIntegerField("кол-во доступных номеров", default=1)

    class Meta:
        verbose_name = "тип номера"
        verbose_name_plural = "типы номеров"
        unique_together = ['hotel', 'name']

    def __str__(self):
        return f"{self.name} ({self.hotel.name}) — {self.price_per_night} ₽/ночь"


class Booking(models.Model):
    """Бронь номера в отеле"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField("дата заезда")
    check_out = models.DateField("дата выезда")
    guests = models.PositiveSmallIntegerField("количество гостей", validators=[MinValueValidator(1)])
    total_price = models.DecimalField("общая стоимость", max_digits=12, decimal_places=2, editable=False)
    status = models.CharField(
        "статус",
        max_length=20,
        choices=[
            ('pending', 'Ожидает подтверждения'),
            ('confirmed', 'Подтверждено'),
            ('cancelled', 'Отменено'),
            ('completed', 'Завершено'),
        ],
        default='pending'
    )
    created_at = models.DateTimeField("дата создания", auto_now_add=True)
    notes = models.TextField("пожелания гостя", blank=True)

    class Meta:
        verbose_name = "бронь"
        verbose_name_plural = "брони"
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                check=models.Q(check_out__gt=models.F('check_in')),
                name='check_out_after_check_in'
            )
        ]

    def save(self, *args, **kwargs):
        """Автоматический расчёт общей стоимости"""
        nights = (self.check_out - self.check_in).days
        self.total_price = self.room_type.price_per_night * nights
        super().save(*args, **kwargs)

    def __str__(self):
        return (f"{self.user.username} — {self.room_type} — "
                f"{self.check_in} → {self.check_out} ({self.get_status_display()})")
    

class VerificationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='verification_token')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.user.username}"    