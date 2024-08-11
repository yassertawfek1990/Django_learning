from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from users.models import UserProfile
from django.core.mail import send_mail
# Create your views here.

class form_new_task(forms.Form):
    task = forms.CharField(label="new_task")

#tasks = ["asd","fgh","jkl"]
def get_all_tasks(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request, "todo/index.html", {
        "tasks": request.session["tasks"]
    })

def adding(request):
    if request.method == "POST":
        data = form_new_task(request.POST)
        if data.is_valid():
            task = data.cleaned_data["task"]
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("tasks"))
        else:
            return render(request, "todo/to_add.html", {"form":data})
    else:
        return render(request, "todo/to_add.html", {"form":form_new_task()})
    

def print_user(request):
    user = request.user  # This is the logged-in user
    user_profile = UserProfile.objects.get(user=user)  # Fetch the UserProfile associated with the logged-in user

    send_mail(
    "Subject here",
    "Here is the message.",
    "fokak908070@gmail.com",
    ["yessirahmed95@gmail.com"],
    fail_silently=False,)

    context = {
        'user': user, # this is the name of the user
        'user_profile': user_profile,
    }
    print(user_profile.user.email)
    return render(request, 'todo/profile.html', context)