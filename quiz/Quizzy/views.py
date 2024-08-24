from random import choice, shuffle  # Import choice and shuffle functions for random selections and shuffling lists
from django.shortcuts import render, redirect  # Import render and redirect functions for rendering templates and redirecting
from users.models import UserProfile  # Import the UserProfile model
from webpages.models import OldQuestions  # Import the OldQuestions model
import requests  # Import the requests library for making HTTP requests
from django.core.mail import send_mail  # Import send_mail function for sending emails
import html  # Import the html module for handling HTML escape sequences
from .models import QuestionsBank  # Import the QuestionsBank model

# Function to fetch questions from an external API based on difficulty level and category
def get_questions(level, cat):
    parameters = {
        "amount": 10,  # Number of questions to fetch
        "category": cat,  # Category of the questions
        "difficulty": level,  # Difficulty level of the questions
        "type": "multiple"  # Type of questions (multiple choice)
    }
    response = requests.get("https://opentdb.com/api.php", params=parameters)  # Make a GET request to the API
    response.raise_for_status()  # Raise an exception if the request was unsuccessful
    question_data = response.json()["results"]  # Extract the questions from the response
    return question_data  # Return the fetched questions

# View to handle the quiz logic
def quiz_view(request, level, cat):
    question_index = request.session.get('question_index', 0)  # Get the current question index from the session
    score = request.session.get('score', 0)  # Get the current score from the session
    questions = request.session.get('questions', None)  # Get the list of questions from the session
    the_level = request.session.get('the_level', "")  # Get the selected difficulty level from the session
    request.session['the_level'] = level  # Store the current difficulty level in the session
    category = request.session.get('category', 0)  # Get the selected category from the session
    request.session['category'] = cat  # Store the current category in the session

    if request.method == "POST":  # If the form has been submitted
        selected_answer = request.POST.get('q_answer')  # Get the selected answer from the form
        if selected_answer == questions[question_index - 1]["correct_answer"]:  # Check if the answer is correct
            score += 1  # Increment the score if the answer is correct
        if question_index <= 9:  # If there are more questions
            question = questions[question_index]  # Get the next question
            q = html.unescape(question["question"])  # Unescape HTML in the question text
            answer = html.unescape(question["correct_answer"])  # Unescape HTML in the correct answer
            wrong = html.unescape(question["incorrect_answers"])  # Unescape HTML in the incorrect answers
            wrong.append(answer)  # Add the correct answer to the list of options
            shuffle(wrong)  # Shuffle the answer options
            request.session['question_index'] = question_index + 1  # Update the question index in the session
            request.session['score'] = score  # Update the score in the session
            return render(request, 'Quizzy/test.html', {"question": q, "options": wrong, "n": question_index + 1, 'level': level, 'cat': cat})
        else:
            request.session['score'] = score  # Store the final score in the session
            return redirect("result")  # Redirect to the result page
    else:
        question_index = 0  # Reset the question index
        score = 0  # Reset the score
        questions = get_questions(level, cat)  # Fetch new questions
        request.session['questions'] = questions  # Store the questions in the session
        question = questions[question_index]  # Get the first question
        q = html.unescape(question["question"])  # Unescape HTML in the question text
        answer = html.unescape(question["correct_answer"])  # Unescape HTML in the correct answer
        wrong = html.unescape(question["incorrect_answers"])  # Unescape HTML in the incorrect answers
        wrong.append(answer)  # Add the correct answer to the list of options
        shuffle(wrong)  # Shuffle the answer options
        request.session['question_index'] = question_index + 1  # Update the question index in the session
        request.session['score'] = 0  # Initialize the score to 0
        return render(request, 'Quizzy/test.html', {"question": q, "options": wrong, "n": question_index + 1, 'level': level, 'cat': cat})

# View to display quiz categories based on the selected difficulty level
def categories(request, level):
    all_categories = {"Vehicles": 28, "Animals": 27, "celebrities": 26, "Art": 25, "Politics": 24, "History": 23, "Geography": 22, "Sports": 21, "General Knowledge": 9}
    return render(request, 'Quizzy/categories.html', {"level": level, "cats": all_categories})

# View to render the main quiz page
def play(request):
    return render(request, 'Quizzy/quizpage.html')

# View to start a quiz with random category and difficulty level
def random(request):
    random_category = choice([9, 21, 22, 23, 24, 25, 26, 27, 28])  # Randomly select a category
    random_level = choice(["easy", "medium", "hard"])  # Randomly select a difficulty level
    return redirect('game', level=random_level, cat=random_category)  # Redirect to the quiz view with random settings

# View to display a form for user-submitted questions
def users_q(request):
    all_categories = ["Vehicles", "Animals", "celebrities", "Art", "Politics", "History", "Geography", "Sports", "General_Knowledge"]
    return render(request, 'Quizzy/users_questions.html', {"cats": all_categories})

# View to handle the submission of user-created quiz questions
def add_q(request, category):
    if request.method == "POST":  # If the form has been submitted
        bank = QuestionsBank()  # Create a new QuestionsBank object
        bank.category = category  # Set the category of the question
        bank.questions = request.POST.get('question')  # Get the question text from the form
        bank.option1 = request.POST.get('option1')  # Get the first option from the form
        bank.option2 = request.POST.get('option2')  # Get the second option from the form
        bank.option3 = request.POST.get('option3')  # Get the third option from the form
        bank.option4 = request.POST.get('option4')  # Get the fourth option from the form
        bank.answer = request.POST.get('answer')  # Get the correct answer from the form
        bank.save()  # Save the question to the database
        return render(request, "webpages/thanks.html")  # Render a thank you page after submission

    return render(request, "Quizzy/add_question.html", {"cat": category})  # Render the add question form if not submitted

# View to handle the quiz logic for user-submitted questions
def play_users(request, category):
    question_index = request.session.get('question_index', 0)  # Get the current question index from the session
    score = request.session.get('score', 0)  # Get the current score from the session

    try:
        questions = list(QuestionsBank.objects.filter(category=category))  # Fetch all questions in the selected category
        if request.method == "POST":  # If the form has been submitted
            selected_answer = request.POST.get('q_answer')  # Get the selected answer from the form
            if selected_answer == questions[question_index - 1].answer:  # Check if the answer is correct
                score += 1  # Increment the score if the answer is correct

            if question_index < len(questions):  # If there are more questions
                question = questions[question_index]  # Get the next question
                wrong = []
                q = html.unescape(question.questions)  # Unescape HTML in the question text
                wrong.append(html.unescape(question.option1))  # Unescape and add the first option
                wrong.append(html.unescape(question.option2))  # Unescape and add the second option
                wrong.append(html.unescape(question.option3))  # Unescape and add the third option
                wrong.append(html.unescape(question.option4))  # Unescape and add the fourth option
                shuffle(wrong)  # Shuffle the answer options
                request.session['question_index'] = question_index + 1  # Update the question index in the session
                request.session['score'] = score  # Update the score in the session
                return render(request, 'Quizzy/test.html', {"question": q, "options": wrong, "n": question_index + 1, 'cat': category})
            else:
                request.session['score'] = score  # Store the final score in the session
                return redirect("result_category", category=category)  # Redirect to the result page
        else:
            score = 0  # Reset the score
            question_index = 0  # Reset the question index
            question = questions[question_index]  # Get the first question
            wrong = []
            q = html.unescape(question.questions)  # Unescape HTML in the question text
            wrong.append(html.unescape(question.option1))  # Unescape and add the first option
            wrong.append(html.unescape(question.option2))  # Unescape and add the second option
            wrong.append(html.unescape(question.option3))  # Unescape and add the third option
            wrong.append(html.unescape(question.option4))  # Unescape and add the fourth option
            shuffle(wrong)  # Shuffle the answer options
            request.session['question_index'] = question_index + 1  # Update the question index in the session
            request.session['score'] = 0  # Initialize the score to 0
            return render(request, 'Quizzy/test.html', {"question": q, "options": wrong, "n": question_index + 1, 'cat': category})
    except:
        return render(request, 'Quizzy/no_questions.html', {"cat": category})  # Render a no questions available page if an error occurs

# View to handle the quiz results
def resulting(request, category=None):
    data = []
    if category is None:
        questions = request.session['questions']  # Get the questions from the session
        for item in questions:
            data.append([html.unescape(item["question"]), html.unescape(item["correct_answer"])])  # Store the questions and answers in data
    else:
        questions = list(QuestionsBank.objects.filter(category=category))  # Fetch questions in the selected category
        data = []
        for question in questions:
            data.append([html.unescape(question.questions), html.unescape(question.answer)])  # Store the questions and answers in data

    if request.user.is_authenticated:  # If the user is logged in
        old_queryset = list(UserProfile.objects.order_by('-total_score'))  # Get the list of users ordered by total score
        user_profile = UserProfile.objects.get(user=request.user.id)  # Get the UserProfile of the logged-in user
        old_rank = old_queryset.index(user_profile) + 1  # Get the user's old rank
        user_profile.total_score += request.session['score']  # Add points to the user's total score
        user_profile.save()  # Save the updated profile
        new_queryset = list(UserProfile.objects.order_by('-total_score'))  # Get the updated list of users ordered by total score
        new_rank = new_queryset.index(user_profile) + 1  # Get the user's new rank
        if new_rank < old_rank:  # If the user's rank has improved
            send_mail(
                "Your Ranking improved",
                f"Congratulations you have improved your ranking\n your old ranking was {old_rank} and your new ranking is {new_rank}",
                "fokak908070@gmail.com",
                [user_profile.user.email],  # Send an email notification to the user
                fail_silently=False,)

        for row in data:
            user_data = OldQuestions(user=request.user, Question=row[0], Answer=row[1])  # Save each question and answer to OldQuestions
            user_data.save()

    else:
        user_profile = None  # Set the user profile to None if not authenticated
        old_rank = None  # Set the old rank to None if not authenticated
        new_rank = None  # Set the new rank to None if not authenticated

    if category is None:  # If the quiz was not category-specific
        return render(request, 'Quizzy/result.html', {"all": data, "the_score": request.session['score'], "info": user_profile, "old": old_rank, "new": new_rank, "level": request.session['the_level'], "category": request.session['category']})
    else:  # If the quiz was category-specific
        return render(request, 'Quizzy/result.html', {"all": data, "the_score": request.session['score'], "info": user_profile, "old": old_rank, "new": new_rank, "category": category})
