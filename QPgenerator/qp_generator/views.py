from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import forms
from . import models
from .decorator import user_passes_test_message,login_required_message
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
@user_passes_test_message(lambda u : u.profile.role == 'admin',message="not authorized")
def add_questions(request):
    if request.method == 'POST':
        question_form = forms.QuestionForm(request.POST)
        if question_form.is_valid():
            question_form.save()
            question_type = question_form.cleaned_data.get('question_type')
            question_id = question_form.cleaned_data.get('id')
            if question_type == 'mcq' or question_type == 'fb':
                return redirect('add_choices',question_id=question_id)
            else:
                return redirect('menu')
    else:
        question_form = forms.QuestionForm()
        return render(request,'add_question.html',{
            "question_form" : question_form
        })
def add_choices(request,question_id):
    question = models.Question.objects.get(id=question_id)
    ChoiceFormset = inlineformset_factory(models.Question,models.Choice,fields=("choice_text",))
    formset = ChoiceFormset(instance=question)
    if request.method == 'POST':
        formset = ChoiceFormset(request.Post,request.FILES,instance=question)
        if formset.is_valid():
            formset.save()
            return redirect('menu')
    else:
        formset = ChoiceFormset(instance=question)
        return redirect(request,'add_choices.html',{
            "formset" : formset
        })