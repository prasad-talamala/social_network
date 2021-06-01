from django.conf.urls import url
from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.home, name="home"),
    path('timeline/', views.timeline, name="timeline"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("add_post/", views.add_post, name="add_post"),
    path("find_friends/", views.find_friends, name="find_friends"),
    path("follow_user/<name>/", views.follow_user, name="follow_user"),
    path("get_user_name/", views.get_user_name, name="get_user_name"),
]
