from django import forms
from .models import News


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть заголовок новини'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введіть текст новини'}),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Текст новини',
        }
