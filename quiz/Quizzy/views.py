from django.shortcuts import render,redirect
from users.models import UserProfile
import requests
import random
# Create your views here.
from django.http import HttpResponseRedirect
from django.http import HttpResponse


def get_questions():
    parameters = {
        "amount" : 10,
        "category":9, #general knowledge
        "difficulty":"easy",
        "type": "multiple"
    }
    response = requests.get("https://opentdb.com/api.php",params= parameters)
    response.raise_for_status()
    question_data = response.json()["results"]
    return question_data

bank = {}
def quiz_view(request):
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
            random.shuffle(wrong)
            return render(request, 'Quizzy/test.html', {"question": q, "options": wrong, "n":n})
        else:
        # You can now use `selected_answer` for whatever you need, like saving it to a database, processing it, etc.
            return redirect("result")
    else:
        n = 0
        score = 0
        questions = get_questions()
        question = questions[n]
        q = question["question"]
        answer = question["correct_answer"]
        wrong = question["incorrect_answers"]
        wrong.append(answer)
        random.shuffle(wrong)
        return render(request, 'Quizzy/test.html', {"question": q, "options": wrong,"n":n})

def categories(request):
    return render(request,'Quizzy/categories.html')

def play(request):
    return render(request,'Quizzy/quizpage.html')

def resulting(request):
    # all_questions = []
    # correct_answers = []
    data = []
    for item in questions:
        data.append([item["question"],item["correct_answer"]])
        # all_questions.append(item["question"])
        # correct_answers.append(item["correct_answer"])

    if request.user.is_authenticated: 
        user_profile = UserProfile.objects.get(user=request.user)  # Get the UserProfile of the logged-in user
        user_profile.total_score += score  # Add points to the total_score
        user_profile.save()  # Save the updated profile
    return render(request,'Quizzy/result.html',{"all":data, "the_score":score, "info": user_profile })