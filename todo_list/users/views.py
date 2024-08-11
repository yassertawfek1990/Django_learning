from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm 
from .forms import RegisterationUserForm

# Create your views here.
def register_view(request):
    if request.method == "POST": 
        form = RegisterationUserForm(request.POST) 
        if form.is_valid(): 
            form.save() 
            return redirect("tasks")
    else:
        form = RegisterationUserForm()
    return render(request, "users/register.html", { "form": form })


