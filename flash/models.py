# from django.db import models

# Create your models here.
from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User

class ResearchTopic(models.Model):    
    description = RichTextUploadingField()

class Flashcard(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title

class Chapter(models.Model):
    
    flash = models.ForeignKey(Flashcard,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class QuestionAnswer(models.Model):

    chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE,related_name='chapter_question',null=True,blank=True)
    question = RichTextUploadingField()
    answer = RichTextUploadingField()
    option = models.TextField(max_length=100)

class SaveAnswer(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateTimeField(auto_now=True)
    chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE)
    total_right = models.TextField(max_length=50)
    total_wrong = models.TextField(max_length=50)

class Timer(models.Model):

    question = models.ForeignKey(QuestionAnswer,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timer = models.CharField(max_length=50, null=True,blank=True)
    answer = models.BooleanField(default=False)
    date = models.DateField(auto_now=True)
    time_start = models.DateTimeField(auto_now=True,null=True,blank=True)





