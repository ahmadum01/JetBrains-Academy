from django.shortcuts import render, redirect
from django.views import View
from vacancy.models import Vacancy
from django.http import HttpResponse

# Create your views here.


class VacancyView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'vacancy/vacancy.html', context={'data': Vacancy.objects.all()})


class NewVacancyView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return HttpResponse(status=403)
        Vacancy.objects.create(description=request.POST['description'], author=request.user)
        return redirect('/home')
