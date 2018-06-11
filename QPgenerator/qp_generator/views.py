from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from . import forms
from . import models
from .decorator import user_passes_test_message,login_required_message,user_is_admin
from django.forms import modelformset_factory,inlineformset_factory
# Create your views here.
def home(request):
    return render(request,'home.html')
def signup(request):
    if request.method == 'POST':
        user_form = forms.SignupForm(request.POST)
        profile_form = forms.ProfileForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            profile_form = forms.ProfileForm(request.POST,instance=user.profile)
            profile_form.full_clean()
            profile_form.save()
            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        user_form = forms.SignupForm()
        profile_form = forms.ProfileForm()
    context = {
            'user_form' : user_form,
            'profile_form' : profile_form
        }
    return render(request,'signup.html',context)

@login_required_message
def menu(request):
    return render(request,'menu.html')


@login_required_message
@user_is_admin
def manage_questions(request,question_id=None,grade_id=None,subject_id=None,chapter_id=None):
    if question_id:
        q = get_object_or_404(models.Question,pk=question_id)  
    else:
        q = None
    ChoiceFormset = inlineformset_factory(models.Question,models.Choice,fields=("choice_text",),max_num=4,extra=4)
    MatchFormset = inlineformset_factory(models.Question,models.Match,fields=("question_text","answer_text","image",),max_num=4,extra=4)
    if request.method == 'POST':
        question_form = forms.QuestionForm(request.POST,request.FILES,instance=q)
        chapter_form = forms.QuestionListForm(request.POST)
        if question_form.is_valid() and chapter_form.is_valid():
            question = question_form.save(commit=False)
            question.school = request.user.profile.school
            chapter = chapter_form.cleaned_data.get('chapter').id
            question.chapter_id = chapter

            if question.question_type == 'mcq' or question.question_type == 'fb':
                choice_formset = ChoiceFormset(request.POST,request.FILES,instance=question)
                if choice_formset.is_valid():
                    question.save()
                    choice_formset.save()
                if 'save_and_add_another' in request.POST:
                    return redirect('manage_questions_autofill',grade_id=question.chapter.grade_id,chapter_id=question.chapter_id,subject_id=question.chapter.subject_id)
                else:
                    return redirect('home')

            elif question.question_type == 'Match':
                match_formset = MatchFormset(request.POST,request.FILES,instance=question)
                if match_formset.is_valid():
                    question.save()
                    match_formset.save()
                if 'save_and_add_another' in request.POST:
                    return redirect('manage_questions_autofill',grade_id=question.chapter.grade_id,chapter_id=question.chapter_id,subject_id=question.chapter.subject_id)
                else:
                    return redirect('home')

            else:
                question.save()
                if 'save_and_add_another' in request.POST:
                    return redirect('manage_questions_autofill',grade_id=question.chapter.grade_id,chapter_id=question.chapter_id,subject_id=question.chapter.subject_id)
                else:
                    return redirect('home')
    else:
        question_form = forms.QuestionForm(instance=q)
        choice_formset = ChoiceFormset(instance=q)
        match_formset =MatchFormset(instance=q)
        if not q:
            if grade_id and chapter_id and subject_id:
                chapter_form = forms.QuestionListForm({
                    "grade" : grade_id,
                    "subject" : subject_id,
                    "chapter" : chapter_id
                })
            else:
                chapter_form = forms.QuestionListForm()
        else:
            chapter_form = forms.QuestionListForm({
                "grade" : q.chapter.grade_id,
                "subject" : q.chapter.subject_id,
                "chapter" : q.chapter_id
            })
    if question_id:
        action = reverse('update_questions',args=[question_id])
    else:
        action = reverse('manage_questions')
    return render(request,'manage_question.html',{
            "question_form" : question_form,
            "chapter_form" : chapter_form,
            "choice_formset" : choice_formset,
            "match_formset" : match_formset,
            "action" : action
    })

@login_required_message
@user_is_admin
def manage_choices(request, question_id):
    question = models.Question.objects.get(id=question_id)
    max=2
    if question.question_type == 'mcq':
        max=4
    ChoiceFormset = inlineformset_factory(models.Question,models.Choice,fields=("choice_text",),max_num=max,extra=max)
    if request.method == 'POST':
        formset = ChoiceFormset(request.POST,request.FILES,instance=question)
        if formset.is_valid():
            formset.save()
            return redirect('menu')
    else:
        formset = ChoiceFormset(instance=question)
    return render(request,'manage_choices.html',{
            "formset" : formset
        })
"""
@login_required_message
@user_is_admin
def manage_matches(request, question_id):
    question = models.Question.objects.get(id=question_id)
    MatchFormset = inlineformset_factory(models.Question,models.Match,fields=("question_text","answer_text","image",),max_num=4,extra=4)
    if request.method == 'POST':
        formset = MatchFormset(request.POST,request.FILES,instance=question)
        if formset.is_valid():
            formset.save()
            return redirect('menu')
    else:
        formset = MatchFormset(instance=question)
    return render(request,'manage_choices.html',{
            "formset" : formset
        })

@login_required_message
def view_questions(request):
    form = forms.QuestionListForm()
    return render(request,'qlist.html',{
        "form" : form 
    })

@login_required_message
@user_is_admin
def manage_chapters(request,ch_id=None):
    if ch_id:
        c=get_object_or_404(models.Chapter,pk=ch_id)
    else:
        c=None
    if request.method == 'POST':
        ch_form = forms.ChapterForm(request.POST,instance=c)
        if ch_form.is_valid():
            ch = ch_form.save(commit=False)
            ch.school = request.user.profile.school
            ch.save()
            return redirect('menu')
    else:
        if c:
            action = reverse('update_chapters',args=[ch_id])
        else:
            action = reverse('manage_chapters')
        ch_form = forms.ChapterForm(instance=c)
        #import pdb; pdb.set_trace()
    return render(request,'manage_chapters.html',{
        'ch_form' : ch_form
    })
"""
def generate_test(request):
    test_details_form = forms.TestForm()
    school = request.user.profile.school
    return render(request,'generate_test.html',{
        'test_details_form' : test_details_form,
        'school' : school,
    })
