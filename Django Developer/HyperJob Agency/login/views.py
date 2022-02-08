from django.shortcuts import render
from django.contrib.auth.views import LoginView

# Create your views here.


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login/login.html'

