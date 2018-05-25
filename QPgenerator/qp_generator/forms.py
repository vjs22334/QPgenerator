from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ('school','role')

class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        exclude = ('created_date','school','chapter')

class QuestionListForm(forms.Form):
    grade=forms.ModelChoiceField(queryset=models.Grade.objects.all())
    subject=forms.ModelChoiceField(queryset=models.Subject.objects.none())
    chapter=forms.ModelChoiceField(queryset=models.Chapter.objects.none())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'grade' in self.data:
            try:
                grade_id = int(self.data.get('grade'))
                self.fields['subject'].queryset = models.Subject.objects.filter(grade_id=grade_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        
        if 'subject' in self.data:
            try:
                subject_id = int(self.data.get('subject'))
                self.fields['chapter'].queryset = models.Chapter.objects.filter(subject_id=subject_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset

        if 'chapter' in self.data:
            self.fields['chapter'].initial = int(self.data.get('chapter'))

class ChapterForm(forms.ModelForm):
    class Meta:
        model = models.Chapter
        exclude = ('school',)

    def __init__(self,*args,**kwargs):
        super(ChapterForm,self).__init__(*args,**kwargs)
        self.fields['subject'].queryset = models.Subject.objects.none()
        if 'grade' in self.data:
            try:
                grade_id = int(self.data.get('grade'))
                self.fields['subject'].queryset = models.Subject.objects.filter(grade_id=grade_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['subject'].queryset = self.instance.grade.subject_set.all()
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
