from .forms import RegistrationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout
from django.urls import reverse

# View for displaying the homepage with any flashed messages
def index(request):
    messages_to_display = messages.get_messages(request)  # Retrieve any messages stored in the session
    return render(request, "index.html", {"messages": messages_to_display})  # Render the homepage with messages

# View for handling user registration
def register_user(request):
    form = RegistrationForm()  # Initialize an empty registration form
    if request.method == "POST":  # Check if the form is submitted
        form = RegistrationForm(request.POST)  # Bind the form with the submitted data
        if form.is_valid():  # Validate the form
            user = form.save(commit=False)  # Create a user object without saving to the database yet
            user.is_active = False  # Set the user as inactive until email confirmation
            user.save()  # Save the user to the database
            
            current_site = get_current_site(request)  # Get the current site domain
            mail_subject = "Activate your account"  # Email subject
            message = render_to_string("registration/account_activation_email.html", {  # Render the email content
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),  # Encode the user's primary key
                "token": account_activation_token.make_token(user)  # Generate a token for email verification
            })
            to_email = form.cleaned_data.get("email")  # Get the user's email from the form
            email = EmailMessage(mail_subject, message, to=[to_email])  # Create an email object
            email.send()  # Send the email
            
            messages.success(request, "Please check your email to complete the registration.")  # Flash a success message
            return redirect("index")  # Redirect to the homepage
    
    return render(request, "registration/register.html", {"form": form})  # Render the registration page with the form

# View for handling account activation via email link
def activate(request, uidb64, token):
    User = get_user_model()  # Get the user model (custom or default)
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  # Decode the user ID from the URL
        user = User.objects.get(pk=uid)  # Retrieve the user from the database
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None  # Handle exceptions where the user doesn't exist or the UID is invalid
        
    if user is not None and account_activation_token.check_token(user, token):  # Validate the token
        user.is_active = True  # Activate the user account
        user.save()  # Save the updated user object
        
        login(request, user)  # Log the user in
        messages.success(request, "Your account has been successfully activated!")  # Flash a success message
        return redirect(reverse("login"))  # Redirect to the login page
    else:
        messages.error(request, "Activation link is invalid or expired.")  # Flash an error message
        return redirect("index")  # Redirect to the homepage

# View for handling user logout
def logout_view(request):
    logout(request)  # Log the user out
    return redirect("main")  # Redirect to the main page
