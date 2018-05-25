from django.contrib.auth import views as auth_views
from django.urls import path
from . import views,ajax_views


urlpatterns=[
    path('',views.home,name="home"),
    path('accounts/login/',auth_views.login,name="login"),
    path('accounts/logout/',auth_views.logout,name="logout"),
    path('accounts/register/',views.signup,name = "signup"),
    path('menu/',views.menu,name="menu"),
    path('manage_questions/',views.manage_questions,name="manage_questions"),
    path('<int:question_id>/manage_choices/', views.manage_choices, name='manage_choices'),
    path('<int:question_id>/manage_matches/', views.manage_matches, name='manage_matches'),
    path('view_questions/', views.view_questions, name='view_questions'),
    path('load_subjects/', ajax_views.load_subjects, name='load_subjects'),
    path('load_chapters/', ajax_views.load_chapters, name='load_chapters'),
    path('load_questions/', ajax_views.load_questions, name='load_questions'),
    path('<int:question_id>/update_question/', views.manage_questions, name='update_questions'),
    path('<int:ch_id>/update_chapter/', views.manage_chapters, name='update_chapters'),
    path('manage_chapters/',views.manage_chapters,name="manage_chapters"),
    path('generate_test/',views.generate_test,name="generate_test"),
]