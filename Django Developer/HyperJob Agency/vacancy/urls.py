from django.urls import path
from vacancy.views import VacancyView, NewVacancyView
from django.views.generic import RedirectView

urlpatterns = [
    path('vacancies/', VacancyView.as_view()),
    path('vacancy/new', NewVacancyView.as_view()),
    path('vacancy/new/', RedirectView.as_view(url='/vacancy/new'))
]
