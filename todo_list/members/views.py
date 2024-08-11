from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm  # only has username and password fields

# Create your views here.
def register_view(request):
    if request.method == "POST": 
        form = UserCreationForm(request.POST) 
        if form.is_valid(): 
            form.save() 
            return redirect("todo:tasks")
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", { "form": form })
