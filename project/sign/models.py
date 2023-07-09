from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")  # опционально, можно не указывать
    last_name = forms.CharField(label="Фамилия")  # опционально

    class Meta:
        model = User
        fields = ("username",
                  "first_name",  # опционально
                  "last_name",  # опционально
                  "email",
                  "password1",
                  "password2",)



# Добавляем пользователя в группу по умолчанию при регистрации
class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get_or_create(name='common')[0]
        basic_group.user_set.add(user)
        return user
from django.db import models

# Create your models here.
