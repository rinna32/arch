from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'blogs'
urlpatterns = [
    # Домашняя страница
    path('', views.index, name='index'),
    path('posts/', views.posts, name='posts'),
    path('posts/<int:post_id>/', views.post, name='post'),
    path('new_post/', views.new_post, name='new_post'),
    path('posts/<int:post_id>/new_entry/', views.new_entry, name='new_entry'),
    path('entry/<int:entry_id>/edit/', views.edit_entry, name='edit_entry'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)