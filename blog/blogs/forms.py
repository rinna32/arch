from django import forms
from .models import BlogPost,Entry

class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'text', 'image']
        labels = {
            'title': 'Название',
            'text': 'Содержимое',
            'image': 'Изображение',
        }
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80}),
        }
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': 'Содержимое'}
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80}),
        }