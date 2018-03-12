from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ask', views.newQuestion, name='newQuestion'),
    path('question', views.question, name='question'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
]