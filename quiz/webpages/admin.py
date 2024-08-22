from django.contrib import admin

# Register your models here.
from .models import Contact,OldQuestions

admin.site.register(OldQuestions)
admin.site.register(Contact)