from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import RegisterForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


class RegisterView(CreateView):
   model = User
   form_class = RegisterForm
   #template_name = 'sign/register.html'
   success_url = '/'

   def form_valid(self, form):
       user = form.save()
       # group = Group.objects.get(name='my_group') # Обращаемся к БД, находим нужную группу. Может оказаться, что такой группы в БД нет. Тогда получим ошибку. Надёжнее использовать метод get_or_create. Обратите внимание, что этот метод возвращает кортеж, поэтому мы обращаемся к первому элементу кортежа через скобки.
       group = Group.objects.get_or_create(name='my_group')[0]

       user.groups.add(group)  # добавляем нового пользователя в эту группу
       user.save()
       return super().form_valid(form)


class LoginView(FormView):
    model = User
    form_class = LoginForm
    template_name = 'sign/login.html'
    success_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, TemplateView):
    template_name = 'sign/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)



# Добавляем функциональное представление для повышения привилегий пользователя до членства в группе
@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        return context



