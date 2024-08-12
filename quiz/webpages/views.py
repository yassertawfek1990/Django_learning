from django.shortcuts import render
from .models import Contact,Suggests 
from .forms import Suggest
from django.http import HttpResponse
# Create your views here.
def home(request):
    return render(request, "webpages/home.html")

def contact_us(request):
    if request.method == "POST":
        contact = Contact()
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('content')
        contact.name = name
        contact.email = email
        contact.content = content
        contact.save()
        return render(request, "webpages/thanks.html")

    return render(request, "webpages/contact.html")

def about_us(request):
    return render(request, "webpages/about.html")

def suggestion(request):
    if request.method == "POST":
        form = Suggest(request.POST)
        if form.is_valid(): 
            form.save() 
            return render(request, "webpages/thanks.html")
    else:
        form = Suggest()    
    return render(request, "webpages/suggest.html", {"form":form})


def register_view(request):
    if request.method == "POST": 
        form = RegisterationUserForm(request.POST) 
        if form.is_valid(): 
            form.save() 
            return redirect("tasks")
    else:
        form = RegisterationUserForm()
    return render(request, "users/register.html", { "form": form })