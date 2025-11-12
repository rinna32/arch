# bookings/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

# Роутер для ViewSet
router = DefaultRouter()
router.register(r'hotels', views.HotelViewSet, basename='hotel')
router.register(r'bookings', views.BookingViewSet, basename='booking')

urlpatterns = [
    # === Аутентификация ===
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # === Загрузка отелей (если есть) ===
    # path('load-hotels/', views.LoadHotelsView.as_view(), name='load_hotels'),

    # === API ===
    path('', include(router.urls)),  # /api/auth/hotels/, /api/auth/bookings/
]