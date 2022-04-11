
from django.http import HttpResponse
from django.shortcuts import render


# Create your views
def home(request):
    return render(request,"home.html")


