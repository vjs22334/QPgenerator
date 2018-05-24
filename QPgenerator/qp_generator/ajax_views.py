from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import forms
from . import models
from .decorator import user_passes_test_message,login_required_message,user_is_admin
from django.forms import modelformset_factory,inlineformset_factory

def load_subjects(request):
    grade_id = request.GET.get('grade')
    grade = models.Grade.objects.get(id=grade_id)
    subject_list = grade.subject_set.all()
    values=[]
    names=[]
    for subject in subject_list:
        values.append(subject.id)
        names.append(subject.subject_name)
    return render(request,'ajax/select_box.html',{
        'list' : zip(values,names)
        
    })
def load_chapters(request):
    grade_id = request.GET.get('grade')
    subject_id = request.GET.get('subject')
    grade = models.Grade.objects.get(id=grade_id)
    subject = models.Subject.objects.get(id=subject_id)
    chapter_list = subject.chapter_set.all()
    chapter_list = chapter_list.filter(subject=subject)
    print(chapter_list)
    values=[]
    names=[]
    for chapter in chapter_list:
        values.append(chapter.id)
        names.append(chapter.ch_name)
    return render(request,'ajax/select_box.html',{
        'list' : zip(values,names)
    })
def load_questions(request):
    chapter_id = request.GET.get('chapter')
    chapter = models.Chapter.objects.get(id=chapter_id)
    questions = models.Question.objects.filter(chapter=chapter)
    return render(request,'ajax/list.html',{
        'questions' : questions
    })