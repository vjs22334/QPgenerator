from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from . import forms
from . import models
from .decorator import user_passes_test_message,login_required_message,user_is_admin
from django.forms import modelformset_factory,inlineformset_factory
from .decorator import user_passes_test_message,login_required_message,user_is_admin
from random import randrange,shuffle
#@login_required_message
#@user_is_admin
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

#@login_required_message
#@user_is_admin
def load_chapters(request):
    grade_id = request.GET.get('grade')
    subject_id = request.GET.get('subject')
    grade = models.Grade.objects.get(id=grade_id)
    subject = models.Subject.objects.get(id=subject_id)
    chapter_list = subject.chapter_set.all()
    chapter_list = chapter_list.filter(grade=grade)
    values=[]
    names=[]
    for chapter in chapter_list:
        values.append(chapter.id)
        names.append(chapter.ch_name)
    return render(request,'ajax/select_box.html',{
        'list' : zip(values,names)
    })

#@login_required_message
#@user_is_admin
def load_questions(request):
    chapter_id = request.GET.get('chapter')
    chapter = models.Chapter.objects.get(id=chapter_id)
    questions = models.Question.objects.filter(chapter=chapter)
    #questions = questions.filter(school=request.user.profile.school)
    return render(request,'ajax/list.html',{
        'questions' : questions
    })

def load_chapters_test(request):
    school = request.user.profile.school
    grade_id = request.GET.get('grade')
    subject_id = request.GET.get('subject')
    q_type = request.GET.get('type')
    grade = models.Grade.objects.get(id=grade_id)
    subject = models.Subject.objects.get(id=subject_id)
    chapter_list = subject.chapter_set.all()
    chapter_list = chapter_list.filter(grade=grade)
   # import pdb; pdb.set_trace()
    ids = []
    names = []
    easy = []
    medium = []
    hard = []
    for chapter in chapter_list:
        ids.append(chapter.id)
        names.append(chapter.ch_name)
        easy.append(chapter.question_set.filter(school = school,difficulty='easy',question_type=q_type).count())
        medium.append(chapter.question_set.filter(school = school,difficulty='medium',question_type=q_type).count())
        hard.append(chapter.question_set.filter(school = school,difficulty='hard',question_type=q_type).count())
    data = {
        "ids" : ids,
        "names" : names,
        "easy" : easy,
        "medium": medium,
        "hard": hard
    }
    return JsonResponse(data)
def random_questions(request):
    c_list = request.GET.getlist("chapters_list[]",[])
    c_list = [json.loads(q) for q in c_list]
    id_list = [c["id"] for c in c_list]
    q_type = request.GET.get("type")
    school = request.user.profile.school
    chapters = models.Chapter.objects.filter(id__in = id_list).prefetch_related("question_set")
    chapters = dict([(obj.id, obj) for obj in chapters])
    for c in c_list:
        chapter = chapters[c['ch_id']]
        q_list = {}
        q_set = [ q for q in chapter.question_set if q.question_type==q_type and q.school==school] 
        q_list['easy'] = [ q for q in q_set if q.difficulty=="easy" ]
        q_list['hard'] = [ q for q in q_set if q.difficulty=="hard"]
        q_list['medium'] = [ q for q in q_set if q.difficulty=="medium"]
        rand_q_list = []
        rand_q_list.append(randList(q_list["easy"],c['easy']))
        rand_q_list.append(randList(q_list["medium"],c['medium']))
        rand_q_list.append(randList(q_list["hard"],c['hard']))
        shuffle(rand_q_list)
        return render(request,"ajax/questions_for_paper.html",{
            "list":rand_q_list
        })
def randList(sample,k):
    result = []
    while len(result)<k:
        n=randrange(len(sample))
        result.append(sample[n])
        sample[n]=sample[-1]
        del sample[-1]
    return result
