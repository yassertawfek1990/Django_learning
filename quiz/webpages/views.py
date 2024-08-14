from django.shortcuts import render
from .models import Contact,Suggests
from users.models import UserProfile
from .forms import Suggest
from django.http import HttpResponse
# Create your views here.
def home(request):
    top_3_values = UserProfile.objects.order_by('-total_score')[:3]

    return render(request, "webpages/home.html", {"scores":top_3_values})

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

    return render(request, "webpages/contact.html",{"form":"contact"})

def about_us(request):
    return render(request, "webpages/about.html")

def suggestion(request):
    if request.method == "POST":
        Suggest = Suggests()
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('content')
        Suggest.name = name
        Suggest.email = email
        Suggest.content = content
        Suggest.save()
        return render(request, "webpages/thanks.html")

    return render(request, "webpages/contact.html")

def all_scores(request):
    all = UserProfile.objects.order_by('-total_score')
    return render(request, "webpages/scores.html",{"values":all ,"n":0})