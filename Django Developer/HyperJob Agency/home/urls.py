from django.urls import path
from home.views import HomeView
from django.views.generic import RedirectView

urlpatterns = [
    path('home', HomeView.as_view()),
    path('home/', RedirectView.as_view(url='/home')),
]