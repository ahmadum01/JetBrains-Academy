from django.shortcuts import render
from django.views import View
# Create your views here.


class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = {'is_auth': request.user.is_authenticated,
                   'is_staff': request.user.is_staff}
        return render(request, 'home/home.html', context=context)
