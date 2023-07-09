from django.urls import path
from .views import RegisterView, LoginView, LogoutView

from .views import IndexView
from .views import upgrade_me

app_name = 'sign'
urlpatterns = [
   path('login/', LoginView.as_view(), name='login'),
   path('logout/', LogoutView.as_view(), name='logout'),
   path('signup/', RegisterView.as_view(template_name = 'sign/signup.html'), name='signup'),
   path('upgrade/', upgrade_me, name = 'upgrade')
]

