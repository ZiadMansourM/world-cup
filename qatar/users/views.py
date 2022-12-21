from django import http


# Create your views here.
def login(request):
    return http.HttpResponse("Login Page")

def register(request):
    return http.HttpResponse("Register Page")