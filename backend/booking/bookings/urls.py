# bookings/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'hotels', views.HotelViewSet, basename='hotel')
router.register(r'bookings', views.BookingViewSet, basename='booking')

urlpatterns = [
    # Аутентификация
    path('register/', views.register_view, name='register'),                    
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Подтверждение email
     
    path('verify-email/<str:token>/', views.verify_email_view, name='verify_email'),

    # API
    path('', include(router.urls)),
]
