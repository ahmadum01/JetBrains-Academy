from django.shortcuts import render, redirect
from django.views import View
from resume.models import Resume
from django.http import HttpResponse

# Create your views here.


class ResumeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'resume/resume.html', context={'data': Resume.objects.all()})


class NewResumeView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.is_staff:
            return HttpResponse(status=403)
        Resume.objects.create(description=request.POST['description'], author=request.user)
        return redirect('/home')



