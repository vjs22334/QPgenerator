from django.contrib.auth import views as auth_views
from django.urls import path
from . import views,ajax_views
from QPgenerator import settings



urlpatterns=[
    path('',views.home,name="home"),
    path('accounts/login/',auth_views.login,name="login"),
    path('accounts/logout/',auth_views.logout,name="logout"),
    path('accounts/register/',views.signup,name = "signup"),
    path('menu/',views.menu,name="menu"),
    path('manage_questions/',views.manage_questions,name="manage_questions"),
    path('<int:grade_id>/<int:subject_id>/<int:chapter_id>/manage_questions/',views.manage_questions,name="manage_questions_autofill"),
    path('view_questions/', views.view_questions, name='view_questions'),
    path('load_subjects/', ajax_views.load_subjects, name='load_subjects'),
    path('load_chapters/', ajax_views.load_chapters, name='load_chapters'),
    path('load_questions/', ajax_views.load_questions, name='load_questions'),
    path('<int:question_id>/update_question/', views.manage_questions, name='update_questions'),
    path('<int:ch_id>/update_chapter/', views.manage_chapters, name='update_chapters'),
    path('manage_chapters/',views.manage_chapters,name="manage_chapters"),
    path('generate_test/',views.generate_test,name="generate_test"),
    path('generate_test/',views.generate_test,name="generate_test"),
    path('load_chapters_test/',ajax_views.load_chapters_test,name="load_chapters_test"),
    path('random_questions/',ajax_views.random_questions,name="random_questions"),
    path('to_pdf/',ajax_views.to_pdf,name="to_pdf"),
    path('create_chapter/',ajax_views.create_chapter,name="create_chapter"),
    path('get_all_subjects/',ajax_views.get_grades_and_subjects,name="get_all_subjects"),
    path('view_papers/',views.view_papers,name="view_papers"),
    path('get_papers/',ajax_views.get_papers,name="get_papers"),
    path('get_paper_pdf/',ajax_views.get_paper_pdf,name="get_paper_pdf"),
    path('delete_question/',ajax_views.delete_question,name="delete_question"),
    path('delete_chapter/',ajax_views.delete_chapter,name="delete_chapter"),
]
