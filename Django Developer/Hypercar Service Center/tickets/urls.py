from django.urls import path, re_path
from tickets.views import (WelcomeView, MenuView,
                           GetTicketView, OperatorMenuView,
                           NextTicketView)

urlpatterns = [
    path('welcome/', WelcomeView.as_view()),
    path('menu/', MenuView.as_view()),
    re_path(r'get_ticket/(change_oil|inflate_tires|diagnostic)/', GetTicketView.as_view()),
    path('processing', OperatorMenuView.as_view()),
    path('next/', NextTicketView.as_view())
]
