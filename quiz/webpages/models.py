from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()

    def __str__(self):
        return self.name
    
class Suggests(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()

    def __str__(self):
        return self.name
    

class OldQuestions(models.Model):  
    # username = models.CharField(max_length=150, unique=True)
    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    # email = models.EmailField(default="admin@admin.com")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Question = models.CharField(max_length=1000)
    Answer = models.CharField(max_length=1000)

    def __str__(self):
        return self.user.username
