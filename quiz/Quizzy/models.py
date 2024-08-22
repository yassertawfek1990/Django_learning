from django.db import models


# Create your models here.
class QuestionsBank(models.Model):
    category = models.CharField(max_length=100)
    questions = models.TextField()
    option1 = models.TextField()
    option2 = models.TextField()
    option3 = models.TextField()
    option4 = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.category