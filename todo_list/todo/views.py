from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
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
