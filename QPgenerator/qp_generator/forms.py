from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models


class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2' , 'username']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class ProfileForm(forms.ModelForm):
    school_password = forms.CharField(max_length = 100, label = "School Password",widget = forms.PasswordInput)
    
    def clean_school_password(self):
        #import pdb; pdb.set_trace()
        password1 = self.cleaned_data.get('school_password')
        school = self.cleaned_data.get('school')
        password2 = school.password
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    ('wrong school or password'),
                    code='password_mismatch',
                    )
        return password1

    class Meta:
        model = models.Profile
        fields = ('school',)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        exclude = ('created_date','school','chapter')

class QuestionListForm(forms.Form):
    grade=forms.ModelChoiceField(queryset=models.Grade.objects.order_by("grade_name"))
    subject=forms.ModelChoiceField(queryset=models.Subject.objects.none())
    chapter=forms.ModelChoiceField(queryset=models.Chapter.objects.none())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.initial = ""
        if 'grade' in self.data:
            try:
                grade_id = int(self.data.get('grade'))
                self.fields['subject'].queryset = models.Subject.objects.filter(grade_id=grade_id).order_by("subject_name")
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        
        if 'subject' in self.data:
            try:
                subject_id = int(self.data.get('subject'))
                self.fields['chapter'].queryset = models.Chapter.objects.filter(subject_id=subject_id).order_by("ch_name")
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset

        if 'chapter' in self.data:
            self.fields['chapter'].initial = int(self.data.get('chapter'))

class ChapterForm(forms.ModelForm):
    class Meta:
        model = models.Chapter
        exclude = ('school',)
        labels={
            "ch_name":"Chapter_Name"
        }
    def __init__(self,*args,**kwargs):
        super(ChapterForm,self).__init__(*args,**kwargs)
        self.fields["grade"].initial = ""
        self.fields['subject'].queryset = models.Subject.objects.none()
        if 'grade' in self.data:
            try:
                grade_id = int(self.data.get('grade'))
                self.fields['subject'].queryset = models.Subject.objects.filter(grade_id=grade_id).order_by("grade_name")
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['subject'].queryset = self.instance.grade.subject_set.order_by("subject_name")
            self.fields['subject'].initial = self.instance.subject.id
        
class TestForm(forms.Form):
    heading = forms.CharField(max_length=200,required=True,help_text='heading')
    instructions = forms.CharField(max_length=2000,widget=forms.Textarea,required=True,help_text="instructions for the examinees")
    date = forms.DateField()
    duration = forms.IntegerField(widget=forms.NumberInput,required=True,help_text="durations in hrs")
    grade=forms.ModelChoiceField(queryset=models.Grade.objects.all())
    subject=forms.ModelChoiceField(queryset=models.Subject.objects.none())


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'grade' in self.data:
            try:
                grade_id = int(self.data.get('grade'))
                self.fields['subject'].queryset = models.Subject.objects.filter(grade_id=grade_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset

class PasswordResetForm(forms.Form):
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    new_password1 = forms.CharField(max_length = 100,label=("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(max_length = 100,label=("New password confirmation"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2

class PasswordResetUsernameForm(forms.Form):
    username = forms.CharField(max_length = 100,label=("username"))