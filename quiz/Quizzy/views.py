from random import choice, shuffle
from django.shortcuts import render,redirect
from users.models import UserProfile
import requests
from django.core.mail import send_mail

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
    global same_level
    global same_category
    same_level = level
    same_category = cat
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
            return render(request, 'Quizzy/test.html', {"question": q, "options": wrong, "n":n+1,'level': level,'cat': cat})
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
        return render(request, 'Quizzy/test.html', {"question": q, "options": wrong,"n":n+1,'level': level,'cat': cat})

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
        old_queryset = list(UserProfile.objects.order_by('-total_score'))
        print(old_queryset)
        user_profile = UserProfile.objects.get(user=request.user.id)  # Get the UserProfile of the logged-in user
        print(user_profile)
        old_rank = old_queryset.index(user_profile) + 1
        print(old_rank)
        user_profile.total_score += score  # Add points to the total_score
        user_profile.save()  # Save the updated profile
        new_queryset = list(UserProfile.objects.order_by('-total_score'))
        print(new_queryset)
        new_rank = new_queryset.index(user_profile) + 1
        print(new_rank)
        if new_rank < old_rank:
            send_mail(
                        "Your Ranking improved",
                        f"Congratulations you have improved your ranking\n your old ranking was {old_rank} and your new ranking is {new_rank}",
                        "fokak908070@gmail.com",
                        [user_profile.user.email],
                        fail_silently=False,)
    else:
        user_profile = None
        old_rank = None
        new_rank = None
    return render(request,'Quizzy/result.html',{"all":data, "the_score":score, "info": user_profile, "old":old_rank ,"new":new_rank, "level": same_level, "category": same_category })


def random(request):
    random_category = choice([9,21,22,23,24,25,26,27,28])
    random_level = choice(["easy","medium","hard"])
    return redirect('game', level=random_level, cat=random_category)