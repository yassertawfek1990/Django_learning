from django.shortcuts import render
from .models import Contact, Suggests  # Import the Contact and Suggests models
from users.models import UserProfile  # Import the UserProfile model
from .models import OldQuestions  # Import the OldQuestions model

# View for rendering the home page with the top 3 user scores

def home(request):
    top_3_values = UserProfile.objects.order_by('-total_score')[:3]  # Get the top 3 users by total score
    return render(request, "webpages/home.html", {"scores": top_3_values})  # Render the home page with the top scores

# View for handling the contact us form submission
def contact_us(request):
    if request.method == "POST":  # Check if the form has been submitted via POST
        contact = Contact()  # Create a new Contact object
        name = request.POST.get('name')  # Get the name from the submitted form data
        email = request.POST.get('email')  # Get the email from the submitted form data
        content = request.POST.get('content')  # Get the content/message from the submitted form data
        contact.name = name  # Assign the name to the contact object
        contact.email = email  # Assign the email to the contact object
        contact.content = content  # Assign the content to the contact object
        contact.save()  # Save the contact object to the database
        return render(request, "webpages/thanks.html")  # Render a thank you page after submission
    
    return render(request, "webpages/contact.html", {"form": "contact"})  # Render the contact form page

# View for rendering the "About Us" page
def about_us(request):
    return render(request, "webpages/about.html")  # Render the about us page

# View for handling the suggestion form submission
def suggestion(request):
    if request.method == "POST":  # Check if the form has been submitted via POST
        Suggest = Suggests()  # Create a new Suggests object
        name = request.POST.get('name')  # Get the name from the submitted form data
        email = request.POST.get('email')  # Get the email from the submitted form data
        content = request.POST.get('content')  # Get the content/suggestion from the submitted form data
        Suggest.name = name  # Assign the name to the suggests object
        Suggest.email = email  # Assign the email to the suggests object
        Suggest.content = content  # Assign the content to the suggests object
        Suggest.save()  # Save the suggests object to the database
        return render(request, "webpages/thanks.html")  # Render a thank you page after submission

    return render(request, "webpages/contact.html")  # Render the contact form page if the request method is not POST

# View for displaying all user scores
def all_scores(request):
    all = UserProfile.objects.order_by('-total_score')  # Get all users ordered by total score in descending order
    return render(request, "webpages/scores.html", {"values": all, "n": 0})  # Render the scores page with all user scores

# View for displaying user-specific data
def data(request):
    all_data = OldQuestions.objects.filter(user=request.user)  # Get all questions associated with the logged-in user
    the_user = UserProfile.objects.get(user=request.user)  # Get the UserProfile of the logged-in user
    print(the_user)  # Print the user's profile data to the console (for debugging purposes)
    print(all_data)  # Print the user's questions data to the console (for debugging purposes)
    return render(request, "webpages/user_data.html", {"values": all_data, "userdata": the_user})  # Render the user's data page
