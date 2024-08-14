from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def quiz_view(request):
    if request.method == "POST":
        selected_answer = request.POST.get('q_answer')
        # You can now use `selected_answer` for whatever you need, like saving it to a database, processing it, etc.
        return HttpResponse(f"You selected: {selected_answer}")
    
    return render(request, 'Quizzy/test.html')

def categories(request):
    return render(request,'Quizzy/categories.html')

def play(request):
    return render(request,'Quizzy/quizpage.html')