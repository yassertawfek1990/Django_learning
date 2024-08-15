from random import choice, shuffle
from django.shortcuts import render,redirect
from users.models import UserProfile
import requests

# Create your views here.
from django.http import HttpResponseRedirect
from django.http import HttpResponse


def get_questions(level, cat):
    parameters = {
        "amount" : 10,
        "category":cat, #general knowledge
        "difficulty":level,
        "type": "multiple"
    }
    response = requests.get("https://opentdb.com/api.php",params= parameters)
    response.raise_for_status()
    question_data = response.json()["results"]
    return question_data

bank = {}
def quiz_view(request,level,cat):
    global n
    global questions
    global score

    if request.method == "POST":
        selected_answer = request.POST.get('q_answer')
        print(selected_answer)
        print(questions[n]["correct_answer"])
        if selected_answer == questions[n]["correct_answer"]:
            score += 1
            print(score)
        if n < 9:
            n += 1
            question = questions[n]
            q = question["question"]
            answer = question["correct_answer"]
            wrong = question["incorrect_answers"]
            wrong.append(answer)
            shuffle(wrong)
            return render(request, 'Quizzy/test.html', {"question": q, "options": wrong, "n":n,'level': level,'cat': cat})
        else:
        # You can now use `selected_answer` for whatever you need, like saving it to a database, processing it, etc.
            return redirect("result")
    else:
        n = 0
        score = 0
        questions = get_questions(level,cat)
        question = questions[n]
        q = question["question"]
        answer = question["correct_answer"]
        wrong = question["incorrect_answers"]
        wrong.append(answer)
        shuffle(wrong)
        return render(request, 'Quizzy/test.html', {"question": q, "options": wrong,"n":n,'level': level,'cat': cat})

def categories(request,level):
    all_categories = {"Vehicles": 28,"Animals":27,"celebrities":26,"Art":25,"Politics":24,"History":23,"Geography":22, "Sports":21, "General Knowledge":9}
    return render(request,'Quizzy/categories.html',{"level":level, "cats":all_categories})

def play(request):
    return render(request,'Quizzy/quizpage.html')

def resulting(request):
    # all_questions = []
    # correct_answers = []
    data = []
    for item in questions:
        data.append([item["question"],item["correct_answer"]])
  

    if request.user.is_authenticated: 
        user_profile = UserProfile.objects.get(user=request.user)  # Get the UserProfile of the logged-in user
        user_profile.total_score += score  # Add points to the total_score
        user_profile.save()  # Save the updated profile
    else:
        user_profile = None
    return render(request,'Quizzy/result.html',{"all":data, "the_score":score, "info": user_profile })


def random(request):
    random_category = choice([9,21,22,23,24,25,26,27,28])
    random_level = choice(["easy","medium","hard"])
    return redirect('game', level=random_level, cat=random_category)