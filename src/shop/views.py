from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'base.html')


def test(request):
    return render(request, 'test.html')