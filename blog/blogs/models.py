from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    text = models.TextField(verbose_name="Текст")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Entry(models.Model):
    """Информация, изученная пользователем по теме"""
    topic = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Возвращает строковое представление модели."""
        return f"{self.text[:50]}..."