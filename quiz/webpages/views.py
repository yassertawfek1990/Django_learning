from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "webpages/home.html")

def contact_us(request):
    return render(request, "webpages/contact.html")

def about_us(request):
    return render(request, "webpages/about.html")

def suggestion(request):
    return render(request, "webpages/suggest.html")