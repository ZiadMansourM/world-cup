from django import http

# Create your views here.
def home(request):
    return http.HttpResponse("Hello World")

def about(request):
    return http.HttpResponse("About Page")