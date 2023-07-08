from django.forms import ModelForm, BooleanField
from .models import News


# Создаём модельную форму
class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ['name', 'authorNew','category', 'description']