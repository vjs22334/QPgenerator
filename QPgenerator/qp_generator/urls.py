from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns=[
    path('',views.home,name="home"),
    path('login/',auth_views.login,name="login"),
    path('logout/',auth_views.logout,name="logout"),
    path('register/',views.signup,name="signup"),
]