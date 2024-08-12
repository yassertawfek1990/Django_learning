from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegistrationForm(UserCreationForm):
    
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ["username", "first_name", "email", "last_name","password1", "password2"]
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email address already exists!")
        return email
    
    # Django's form system allows you to create custom validation methods for individual fields by defining a method with the name pattern clean_<fieldname>, where <fieldname> is the name of the form field. In your case, clean_email is the custom validation method for the email field.
    # When the form's is_valid() method is called, Django automatically invokes any clean_<fieldname> methods in the form. For your RegistrationForm, Django will call clean_email during the validation process to ensure that the email meets the specified criteria.
    #If the email does not already exist in the database, the method simply returns the email value. Returning the value is necessary because clean_<fieldname> methods are expected to return the cleaned data for that field. This cleaned email value will be used later in the form processing, like saving the user object.