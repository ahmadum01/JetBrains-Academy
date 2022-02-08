from django.urls import path
from login.views import MyLoginView
from django.views.generic import RedirectView

urlpatterns = [
    path('login', MyLoginView.as_view()),
    path('login/', RedirectView.as_view(url='/login')),
]
