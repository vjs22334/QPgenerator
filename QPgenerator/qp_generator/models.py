from django.db import models


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
        ("subjective","Subjective"),
        ("fb","fill in the blanks"),
        ("Tf","true or false"),
        ("Match","match the following")
    )
    question_text = models.CharField(max_length=2000)
    difficulty = models.CharField(max_length=10, choices=difficulty_choices)
    question_type = models.CharField(max_length=50, choices=type_choices)
    chapter = models.ForeignKey(Chapter,on_delete = models.CASCADE)
    answer = models.TextField(default="no answer")
    image = models.ImageField(upload_to="question",null=True)
    created_date = models.DateTimeField("created date")

    def __str__(self):
        return self.question_text
    