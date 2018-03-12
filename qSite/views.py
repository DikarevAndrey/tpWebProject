from django.http import HttpResponse
from django.shortcuts import render

def index(request):
  return render(request, 'qSite/index.html')

def newQuestion(request):
  return render(request, 'qSite/ask.html')

def question(request):
  return render(request, 'qSite/question.html')

def signin(request):
  return render(request, 'qSite/login.html')

def signup(request):
  return render(request, 'qSite/signup.html')