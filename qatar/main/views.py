from django import http
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'main/home.html',{
        'title':'home'
    })

def about(request):
    return http.HttpResponse("About Page")