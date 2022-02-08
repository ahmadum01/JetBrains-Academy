from django.urls import path
from resume.views import ResumeView, NewResumeView
from django.views.generic import RedirectView

urlpatterns = [
    path('resumes/', ResumeView.as_view()),
    path('resume/new', NewResumeView.as_view()),
    path('resume/new/', RedirectView.as_view(url='/resume/new')),
]