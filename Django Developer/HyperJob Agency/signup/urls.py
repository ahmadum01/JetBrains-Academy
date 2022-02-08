from django.urls import path
from django.views.generic import RedirectView
from signup.views import SignupView

urlpatterns = [
    path('signup', SignupView.as_view()),
    path('signup/', RedirectView.as_view(url='/signup')),
]