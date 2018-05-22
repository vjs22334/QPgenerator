from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns=[
    path('',views.home,name="home"),
    path('accounts/login/',auth_views.login,name="login"),
    path('accounts/logout/',auth_views.logout,name="logout"),
    path('accounts/register/',views.signup,name="signup"),
    path('menu/',views.menu,name="menu"),
    path('Q-add/',views.add_questions,name="add_questions"),
    path('denied/',views.permission_denied,name="permission_denied")
]