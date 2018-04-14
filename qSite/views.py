from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from random import randint
from django.core.paginator import Paginator, EmptyPage
from qSite.models import *
from qSite.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

def paginate(request, objects_list, limit):
  page = request.GET.get('page') or 1

  try:
    page = int(page)
  except ValueError:
    page = 1

  paginator = Paginator(objects_list, limit)
  try:
    page = paginator.get_page(page)
  except EmptyPage:
    page = paginator.get_page(paginator.num_pages)

  return page


def index(request):
  if request.path == '/qsite/hot':
    tab = 'hot'
    questions = Question.objects.hottest()
  else:
    tab = 'new'
    questions = Question.objects.newest()
  page = paginate(request, questions, 20)
  context = {'questions': page.object_list, 'tab': tab, 'page': page}
  return render(request, 'qSite/index.html', context)


def search(request):
  q = request.GET.get('q')
  tags = Tag.objects.search(q)
  users = Profile.objects.search(q)
  questions = Question.objects.search(q)
  context = {'q': q, 'tags': tags, 'users': users, 'questions': questions}
  return render(request, 'qSite/search_list.html', context)


@login_required(login_url='/qsite/signin')
def newQuestion(request):
  form = AskForm(request.POST or None)
  if request.method == "POST":
    if form.is_valid():
      form.instance.author = request.user
      question = form.save()
      return redirect('question', question.id)
  context = {'form': form}
  return render(request, 'qSite/ask.html', context)


def question(request, questionId):
  question = Question.objects.by_id(questionId)
  answers = Answer.objects.hottest(questionId)
  page = paginate(request, answers, 30)
  form = AnswerForm(request.POST or None)
  if request.method == "POST":
    if form.is_valid():
      answer = form.save(commit=False)
      answer.author = request.user
      answer.question = question
      answer.save()
      page_number = answer.get_page()
      return redirect('/qsite/question/' + str(questionId) + '?page=' + str(page_number) + '#answer' + str(answer.id))
  if request.method == "GET" and request.user.is_authenticated:
    #  метод модели - отвечал ли уже is_answered
    if Answer.objects.filter(question__id=questionId, author=request.user).first() is not None:
      form = None
  context = {'question': question, 'answers': page.object_list, 'page': page, 'form': form}
  return render(request, 'qSite/question.html', context)


def signin(request):
  if request.user.is_authenticated:
    return redirect(request.GET.get('next', 'index'))
  else:
    return auth_views.login(request, template_name='qSite/login.html', authentication_form=SignInForm)


def signup(request):
  if request.method == "GET" and request.user.is_authenticated:
    return redirect('index')
  form = SignUpForm(request.POST or None, request.FILES or None)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      user = authenticate(
        request,
        username=form.cleaned_data.get('username'),
        password=form.cleaned_data.get('password1')
      )
      login(request, user)
      return redirect('index')
  context = {'form': form}
  return render(request, 'qSite/signup.html', context)


def signout(request):
  logout(request)
  return redirect(request.META.get('HTTP_REFERER'))


def tag(request, tagName):
  questions = Tag.objects.by_tag_newest(tagName)
  page = paginate(request, questions, 20)
  context = {'questions': page.object_list, 'tag': tagName, 'page': page}
  return render(request, 'qSite/tag.html', context)


def profile(request, userId):
  profile = Profile.objects.by_id(userId)
  questions = profile.get_questions()
  answers = profile.get_answers()
  context = {'profile': profile, 'questions': questions, 'answers': answers}
  return render(request, 'qSite/profile.html', context)

@login_required(login_url='/qsite/signin')
def editProfile(request):
  if request.method == "POST":
    form = EditProfileForm(request.POST, request.FILES, instance=request.user)
    if form.is_valid():
      form.save()
      return redirect('profile', request.user.id)
  else:
    form = EditProfileForm(instance=request.user)
  context = {'form': form}
  return render(request, 'qSite/editProfile.html', context)
