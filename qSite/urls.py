from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ask', views.newQuestion, name='newQuestion'),
    path('profile/<int:userId>', views.profile, name='profile'),
    path('profile/edit', views.editProfile, name='editProfile'),
    path('question/<int:questionId>', views.question, name='question'),
    path('search', views.search, name='search'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('signout', views.signout, name='signout'),
    path('tag/<str:tagName>', views.tag, name='tag'),
    path('hot', views.index, name='hot'),
    path('like', views.like, name='like'),
    path('correct', views.correct, name='correct'),
]