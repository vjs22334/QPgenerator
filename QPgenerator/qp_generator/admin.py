import os
from django.contrib import admin
from .models import Question,Subject,Grade,Chapter,Choice,Match
ENV_PATH = os.path.abspath(os.path.dirname(__file__))

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4
class MatchInline(admin.StackedInline):
    model = Match
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    fieldsets=[
        ("Question details",{'fields':["chapter","question_text","difficulty","question_type"]}),
        ("Optional",{"fields":["answer","image"]}),
        ("Date Info",{"fields":["created_date"]})
    ]
    inlines=[ChoiceInline,MatchInline]
    class Media:
        js = ('js/toggle.js',)
    



admin.site.register(Question,QuestionAdmin)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(Chapter)
admin.site.register(Choice)
admin.site.register(Match)


# Register your models here.
