from random import choice, shuffle
from django.shortcuts import render,redirect
from users.models import UserProfile
from webpages.models import OldQuestions
import requests
from django.core.mail import send_mail
import html
from .models import QuestionsBank
# from .forms import NewQuestion


def get_questions(level, cat):
    parameters = {
        "amount" : 10,
        "category":cat, 
        "difficulty":level,
        "type": "multiple"
    }
    response = requests.get("https://opentdb.com/api.php",params= parameters)
    response.raise_for_status()
    question_data = response.json()["results"]
    return question_data

bank = {}
def quiz_view(request,level,cat):
    
    question_index = request.session.get('question_index', 0)
    score = request.session.get('score', 0)
    questions = request.session.get('questions',None)
    the_level = request.session.get('the_level', "")
    request.session['the_level'] = level
    category = request.session.get('category', 0)
    request.session['category'] = cat
    if request.method == "POST":
        selected_answer = request.POST.get('q_answer')
        if selected_answer == questions[question_index-1]["correct_answer"]:
            score += 1
        if question_index <= 9:
            question = questions[question_index]
            q = html.unescape(question["question"])
            answer = html.unescape(question["correct_answer"])
            wrong = html.unescape( question["incorrect_answers"])
            wrong.append(answer)
            shuffle(wrong)
            request.session['question_index'] = question_index + 1
            request.session['score'] = score
            return render(request, 'Quizzy/test.html', {"question": q, "options": wrong, "n":question_index+1,'level': level,'cat': cat})
        else:
            request.session['score'] = score
            return redirect("result")
    else:
        question_index = 0
        score = 0
        questions = get_questions(level,cat)
        request.session['questions'] = questions
        question = questions[question_index]
        q = html.unescape(question["question"])
        answer = html.unescape(question["correct_answer"])
        wrong = html.unescape(question["incorrect_answers"])
        wrong.append(answer)
        shuffle(wrong)
        request.session['question_index'] = question_index + 1
        request.session['score'] = 0 
        return render(request, 'Quizzy/test.html', {"question": q, "options": wrong,"n":question_index+1,'level': level,'cat': cat})

def categories(request,level):
    all_categories = {"Vehicles": 28,"Animals":27,"celebrities":26,"Art":25,"Politics":24,"History":23,"Geography":22, "Sports":21, "General Knowledge":9}
    return render(request,'Quizzy/categories.html',{"level":level, "cats":all_categories})

def play(request):
    return render(request,'Quizzy/quizpage.html')


def random(request):
    random_category = choice([9,21,22,23,24,25,26,27,28])
    random_level = choice(["easy","medium","hard"])
    return redirect('game', level=random_level, cat=random_category)

def users_q(request):
        all_categories = ["Vehicles","Animals","celebrities","Art","Politics","History","Geography", "Sports", "General_Knowledge"]
        return render(request,'Quizzy/users_questions.html', {"cats":all_categories})

def add_q(request, category):
    if request.method == "POST":
        bank = QuestionsBank()
        bank.category = category
        bank.questions = request.POST.get('question')
        bank.option1 = request.POST.get('option1')
        bank.option2 = request.POST.get('option2')
        bank.option3 = request.POST.get('option3')
        bank.option4 = request.POST.get('option4')
        bank.answer = request.POST.get('answer')
        bank.save()
        return render(request, "webpages/thanks.html")

    return render(request, "Quizzy/add_question.html", {"cat":category})





def play_users(request,category):
    question_index = request.session.get('question_index', 0)
    score = request.session.get('score', 0)

    try :
        questions = list(QuestionsBank.objects.filter(category=category))
        if request.method == "POST":
            selected_answer = request.POST.get('q_answer')
            if selected_answer == questions[question_index - 1].answer:
                score += 1

            if question_index < len(questions):
                question = questions[question_index]
                wrong = []
                q = html.unescape(question.questions)
                wrong.append(html.unescape(question.option1))
                wrong.append(html.unescape(question.option2))
                wrong.append(html.unescape(question.option3))
                wrong.append(html.unescape(question.option4))
                shuffle(wrong)
                request.session['question_index'] = question_index + 1
                request.session['score'] = score
                return render(request, 'Quizzy/test.html', {"question": q, "options": wrong, "n":question_index+1,'cat': category})
            else:
            # we can now use `selected_answer` for whatever we need, like saving it to a database, processing it, etc.
                request.session['score'] = score
                return redirect("result_category",category=category)
            
        else:
            score = 0
            question_index = 0
            question = questions[question_index]
            wrong = []
            q = html.unescape(question.questions)
            wrong.append(html.unescape(question.option1))
            wrong.append(html.unescape(question.option2))
            wrong.append(html.unescape(question.option3))
            wrong.append(html.unescape(question.option4))
            shuffle(wrong)
            request.session['question_index'] = question_index + 1
            request.session['score'] = 0
            return render(request, 'Quizzy/test.html', {"question": q, "options": wrong,"n":question_index+1,'cat': category})
    except:
         return render(request, 'Quizzy/no_questions.html', {"cat":category})

        

def resulting(request, category=None):
    data = []
    if category is None:
        questions = request.session['questions']
        for item in questions:
            data.append([html.unescape(item["question"]),html.unescape(item["correct_answer"])])
    else:
        questions = list(QuestionsBank.objects.filter(category=category))
        data = []
        for question in questions:
            data.append([html.unescape(question.questions), html.unescape(question.answer)])


    if request.user.is_authenticated:
        old_queryset = list(UserProfile.objects.order_by('-total_score'))
        user_profile = UserProfile.objects.get(user=request.user.id)  # Get the UserProfile of the logged-in user
        old_rank = old_queryset.index(user_profile) + 1
        user_profile.total_score += request.session['score']  # Add points to the total_score
        user_profile.save()  # Save the updated profile
        new_queryset = list(UserProfile.objects.order_by('-total_score'))
        new_rank = new_queryset.index(user_profile) + 1
        if new_rank < old_rank:
            send_mail(
                        "Your Ranking improved",
                        f"Congratulations you have improved your ranking\n your old ranking was {old_rank} and your new ranking is {new_rank}",
                        "fokak908070@gmail.com",
                        [user_profile.user.email],
                        fail_silently=False,)
            
        for row in data:
            user_data = OldQuestions(user=request.user, Question = row[0], Answer = row[1])
            user_data.save()
        
        
    else:
        user_profile = None
        old_rank = None
        new_rank = None
    
    if category is None:
        return render(request,'Quizzy/result.html',{"all":data, "the_score":request.session['score'], "info": user_profile, "old":old_rank ,"new":new_rank, "level": request.session['the_level'], "category": request.session['category'] })
    else:
        return render(request,'Quizzy/result.html',{"all":data, "the_score":request.session['score'], "info": user_profile, "old":old_rank ,"new":new_rank, "category": category })
