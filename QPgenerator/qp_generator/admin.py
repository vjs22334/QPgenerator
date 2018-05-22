import os
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Question,Subject,Grade,Chapter,Choice,Match,School,Profile
from django.contrib.auth.models import User
ENV_PATH = os.path.abspath(os.path.dirname(__file__))

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

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
    
class ModUserAdmin(UserAdmin):
    inlines=[ProfileInline]

    def get_inline_instances(self,request,obj=None):
        if not obj:
            return list()
        return super(ModUserAdmin,self).get_inline_instances(request,obj)

admin.site.unregister(User)
admin.site.register(User,ModUserAdmin)


admin.site.register(Question,QuestionAdmin)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(Chapter)
admin.site.register(Choice)
admin.site.register(Match)
admin.site.register(School)
admin.site.register(Profile)


# Register your models here.
