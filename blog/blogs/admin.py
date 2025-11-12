from django.contrib import admin

# Register your models here.
from .models import BlogPost,Entry

# Register your models here.
admin.site.register(BlogPost)
admin.site.register(Entry)