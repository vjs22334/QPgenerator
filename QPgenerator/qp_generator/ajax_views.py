from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from . import forms
from . import models
from .decorator import user_passes_test_message,login_required_message,user_is_admin
from django.forms import modelformset_factory,inlineformset_factory
from .decorator import user_passes_test_message,login_required_message,user_is_admin
from random import randrange,shuffle
import json
from django.core.files.storage import FileSystemStorage
from weasyprint import HTML,CSS
from QPgenerator.settings import MEDIA_ROOT
from os import path
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.conf import settings
@login_required_message
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

@login_required_message
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

@login_required_message
#@user_is_admin
def load_questions(request):
    chapter_id = request.GET.get('chapter')
    chapter = models.Chapter.objects.get(id=chapter_id)
    questions = models.Question.objects.filter(chapter=chapter)
    questions = questions.filter(school=request.user.profile.school)
    new_questions=[]
    for question in questions:
        new_questions.append({
            'question_id':question.id,
            'question_text':question.question_text[0:100],
            'question_diff':question.difficulty,
            'question_type':question.question_type

        })


    return render(request,'ajax/list.html',{
        'questions' : new_questions
    })

@login_required_message
def load_chapters_test(request):
    school = request.user.profile.school
    grade_id = request.GET.get('grade')
    subject_id = request.GET.get('subject')
    q_type = request.GET.get('type')
    grade = models.Grade.objects.get(id=grade_id)
    subject = models.Subject.objects.get(id=subject_id)
    chapter_list = subject.chapter_set.all()
    chapter_list = chapter_list.filter(grade=grade)
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

class MatchQuestion():
    def __init__(self,list,question):
        self.question=question
        self.a_list = []
        self.key_list = []
        self.q_list = []
        i = 0
        for l in list:
            self.a_list.append((l.answer_text,i))
            i+=1
        self.q_list=list

    def shuffle_check(self):
        for i in range(len(self.a_list)):
            if self.a_list[i][1] == i:
                return False
        return True

    def generate_key(self):
        for i in range(len(self.a_list)):
            self.key_list.append((self.a_list[i][1]+1,i+1))
        self.key_list=sorted(self.key_list,key=lambda x:x[0])
    
    def shuffle_ans(self):
        while not self.shuffle_check():
            shuffle(self.a_list)
    
    def merge(self):
        self.q_and_a_list = []
        for i in range(len(self.q_list)):
            self.q_and_a_list.append((self.q_list[i].question_text,self.a_list[i][0],self.q_list[i]))


@login_required_message
def random_questions(request):
    c_list = request.GET.getlist("chapters_list[]",[])
    #import pdb;pdb.set_trace()
    c_list = [json.loads(q) for q in c_list]
    id_list = [c["id"] for c in c_list]
    q_type = request.GET.get("type")
    school = request.user.profile.school
    chapters = models.Chapter.objects.filter(id__in = id_list).prefetch_related("question_set")
    chapters = dict([(obj.id, obj) for obj in chapters])
    rand_q_list = []
    for c in c_list:
        chapter = chapters[c['id']]
        q_list = {}
        q_set = [ q for q in chapter.question_set.all() if q.question_type==q_type and q.school==school] 
        q_list['easy'] = [ q.id for q in q_set if q.difficulty=="easy" ]
        q_list['hard'] = [ q.id for q in q_set if q.difficulty=="hard"]
        q_list['medium'] = [ q.id for q in q_set if q.difficulty=="medium"]
        rand_q_list.extend(randList(q_list["easy"],c['easy']))
        rand_q_list.extend(randList(q_list["medium"],c['medium']))
        rand_q_list.extend(randList(q_list["hard"],c['hard']))
    shuffle(rand_q_list)
    match_list = []
    if q_type == "mcq" or q_type == "fb":
        final_q_list=models.Question.objects.filter(id__in = rand_q_list).prefetch_related("choice_set")
    elif q_type == "Match":
        final_q_list=[]
        q_set=models.Question.objects.filter(id__in = rand_q_list).prefetch_related("match_set")
        #import pdb; pdb.set_trace()
        for q in q_set:
            final_q_list.extend(q.match_set.all())
        #shuffle(final_q_list)
        for i in range(int(len(final_q_list)/4)):
            match_question = MatchQuestion(final_q_list[i*4:(i+1)*4],q_set[i])
            match_question.shuffle_ans()
            match_question.generate_key()
            match_question.merge()
            match_list.append(match_question)                
    else:
        final_q_list=models.Question.objects.filter(id__in = rand_q_list)
    
    if q_type=="Match":
        type_name="Match the following"
    elif q_type=="mcq":
        type_name="Multiple Choice Questions"
    elif q_type=="Tf":
        type_name="True or False"
    elif q_type=="short":
        type_name="Short Answers"
    else:
        type_name="Long Answers"



    return render(request,"ajax/questions_for_paper.html",{
            "list": final_q_list,
            "q_type": q_type,
            "match_list" : match_list,
            "type_name":type_name

        })
def randList(sample,k):
    result = []
    while len(result)<int(k):
        n=randrange(len(sample))
        result.append(sample[n])
        sample[n]=sample[-1]
        del sample[-1]
    return result

@login_required_message
def to_pdf(request):
    html_string = request.GET.get("html_data")
    html = HTML(string=html_string,base_url=request.build_absolute_uri()
    )
    filename = 'Qpaper'+str(timezone.now())+'.pdf'
    file_path = path.join(MEDIA_ROOT,'tmp/')
    absolute_path = path.join(MEDIA_ROOT,'tmp/'+filename)
    html.write_pdf(target=absolute_path,stylesheets=[CSS('/home/raj007/djangogirls/myvenv/bangalore/QPgenerator/QPgenerator/static/css/bootstrap.min.css'),CSS('/home/raj007/djangogirls/myvenv/bangalore/QPgenerator/QPgenerator/static/css/bootstrap.css')])
    grade_id = request.GET.get("grade")
    subject_id = request.GET.get("subject")
    grade = models.Grade.objects.get(id=grade_id)
    subject = models.Subject.objects.get(id=subject_id)
    heading = request.GET.get('heading')
    school = request.user.profile.school
    date = request.GET.get('date')

    fs = FileSystemStorage(path.join(MEDIA_ROOT,'tmp/'))
    with fs.open(filename) as pdf:
        paper = models.Paper.objects.create(heading=heading,grade=grade,subject=subject,school=school,file_path=file_path,file_name=filename,date=date)
        if paper:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
            return response

    return HttpResponse(status="500")

@login_required_message
@user_is_admin
@require_http_methods(['POST',])
def create_chapter(request):
    subject_id = request.POST.get("subject")
    grade_id = request.POST.get("grade")
    ch_name = request.POST.get("ch_name")
    subject = models.Subject.objects.get(id=subject_id)
    grade = models.Grade.objects.get(id=grade_id)
    if subject in grade.subject_set.all():
        chapter = models.Chapter.objects.create(ch_name=ch_name,school=request.user.profile.school,grade=grade,subject=subject)
        if chapter:
            data={
                "success" : True,
                "status_code" : 200,
            }
        else:
            data={
                "success" : False,
                "status_code" : 500,
            }
    else:
        data={
            "success" : False,
            "status_code" : 422,
        }

    return JsonResponse(data)

@login_required_message
def get_grades_and_subjects(request):
    school = request.user.profile.school
    grade_list = list(range(1,school.max_grade))
    grades = models.Grade.objects.filter(grade_name__in = grade_list).prefetch_related("subject_set")
    data = []
    #import pdb;pdb.set_trace()
    for grade in grades:
        subjects = []
        for subject in grade.subject_set.all():
            subjects.append({
                "id":subject.id,
                "name":subject.subject_name
            })
        data.append({
            "id"    : grade.id,
            "grade" : grade.grade_name,
            "subjects" : subjects
        })
    return JsonResponse(data,safe=False)

@login_required_message
def get_papers(request):
    grade_id = request.GET.get("grade")
    subject_id = request.GET.get("subject")
    grade = models.Grade.objects.get(id=grade_id)
    subject = models.Subject.objects.get(id=subject_id)
    school = request.user.profile.school
    paper_list = models.Paper.objects.filter(school = school,grade=grade,subject=subject)
    #import pdb; pdb.set_trace()
    if paper_list: 
        resp_data = []
        for paper in paper_list:
            date=str(paper.created_date)[0:10]
            newdate=date[8:10]
            newdate+=date[4:8]
            newdate+=date[0:4]
            resp_data.append({
                "id" : paper.id,
                "heading" : paper.heading,
                "created_date" : newdate,
                "date" : paper.date
            })
    else:
        resp_data = "404"
    
    return JsonResponse(resp_data,safe=False)

@login_required_message
def get_paper_pdf(request):
    paper_id = request.GET.get('id')
    paper = models.Paper.objects.get(id=paper_id)
    if paper:
        fs = FileSystemStorage(paper.file_path)
        with fs.open(paper.file_name) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
            return response
    else:
        return HttpResponse(status=404)

@login_required_message
@user_is_admin
@require_http_methods(["POST",])
def delete_chapter(request):
    chapter_id = request.POST.get('ch_id')
    chapter = models.Chapter.objects.get(id=chapter_id)
    if chapter:
        chapter.delete()
        resp ={
            "status_code" : 200
        }
    else:
        resp = {
            "status_code" : 404
        }
    return JsonResponse(resp)

@login_required_message
@user_is_admin
@require_http_methods(["POST",])
def delete_question(request):
    question_id = request.POST.get('q_id')
    question = models.Question.objects.get(id=question_id)
    if question:
        question.delete()
        resp ={
            "status_code" : 200
        }
    else:
        resp = {
            "status_code" : 404
        }
    return JsonResponse(resp)
    