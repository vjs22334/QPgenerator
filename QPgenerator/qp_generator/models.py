from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
class School(models.Model):
    school_name = models.CharField(max_length=200,unique=True)
    address = models.TextField()

    def __str__(self):
        return self.school_name
class Profile(models.Model):
    roles = (
        ("admin","admin"),
        ("teacher","teacher")
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School,on_delete=models.CASCADE)
    role = models.CharField(max_length=50,choices=roles)

    def __str__(self):
        return self.user.username'
@receiver(post_save,sender=User)
def update_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance,school=School.objects.get(id=1))
    instance.profile.save()


class Grade(models.Model):
    grade_name = models.CharField(max_length=10)
    
    def __str__(self):
        return self.grade_name

class Subject(models.Model):
    subject_name = models.CharField(max_length=10)
    grade = models.ForeignKey(Grade,on_delete = models.CASCADE)
    
    def __str__(self):
        return self.subject_name 

class Chapter(models.Model):
    ch_name = models.CharField(max_length=500)
    subject = models.ForeignKey(Subject,on_delete = models.CASCADE)
    grade = models.ForeignKey(Grade,on_delete = models.CASCADE)

    def __str__(self):
        return self.ch_name

class Question(models.Model):
    difficulty_choices=(
        ("easy","easy"),
        ("medium","medium"),
        ("hard","hard"),
    )
    type_choices=(
        ("mcq","Mcq"),
        ("short","short answer"),
        ("long","long answer"),
        ("fb","fill in the blanks"),
        ("Tf","true or false"),
        ("Match","match the following")
    )
    question_text = models.TextField(default="match the following")
    difficulty = models.CharField(max_length=10, choices=difficulty_choices)
    question_type = models.CharField(max_length=50, choices=type_choices,default="match the following")
    chapter = models.ForeignKey(Chapter,on_delete = models.CASCADE)
    answer = models.TextField(null=True)
    image = models.ImageField(upload_to="question",null=True)
    created_date = models.DateTimeField("created date")
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    choice_text = models.CharField(max_length = 100)
    question = models.ForeignKey(Question, on_delete = models.CASCADE)

    def __str__(self):
        return self.choice_text
class Match(models.Model):
    question_text = models.CharField(max_length=100)
    answer_text = models.CharField(max_length=100)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="match",null=True)

    def __str__(self):
        return self.question_text    