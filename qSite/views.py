from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from random import randint
from django.core.paginator import Paginator, EmptyPage
from qSite.models import *
from qSite.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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


def add_tags_users_to_context(context):
  top_users = Profile.objects.by_rating()[:3]
  top_tags = Tag.objects.hottest()[:3]
  context['top_users'] = top_users
  context['top_tags'] = top_tags
  return context


def index(request):
  if request.path == '/qsite/hot':
    tab = 'hot'
    questions = Question.objects.hottest()
  else:
    tab = 'new'
    questions = Question.objects.newest()
  page = paginate(request, questions, 20)
  context = {'questions': page.object_list, 'tab': tab, 'page': page}
  context = add_tags_users_to_context(context)
  return render(request, 'qSite/index.html', context)


def search(request):
  q = request.GET.get('q')
  tags = Tag.objects.search(q)
  users = Profile.objects.search(q)
  questions = Question.objects.search(q)
  context = {'q': q, 'tags': tags, 'users': users, 'questions': questions}
  context = add_tags_users_to_context(context)
  return render(request, 'qSite/search_list.html', context)


@login_required(login_url='/qsite/signin')
def newQuestion(request):
  context = add_tags_users_to_context({})
  return render(request, 'qSite/ask.html', context)


def question(request, questionId):
  question = Question.objects.by_id(questionId)
  answers = Answer.objects.hottest(questionId)
  page = paginate(request, answers, 30)
  context = {'question': question, 'answers': page.object_list, 'page': page}
  context = add_tags_users_to_context(context)
  return render(request, 'qSite/question.html', context)


def signin(request):
  form = SignInForm(request.POST or None)
  redirect_to = request.GET.get('next', 'index')
  if request.method == "POST":
    if form.is_valid():
      user = authenticate(request, username=form.cleaned_data.get('login'), password=form.cleaned_data.get('password'))
      if user is not None:
        login(request, user)
        return redirect(redirect_to)
      else:
        form.add_error(None, "Invalid password.")

  context = {'form': form, 'redirect_to': redirect_to}
  context = add_tags_users_to_context(context)
  return render(request, 'qSite/login.html', context)


def signup(request):
  form = SignUpForm(request.POST or None, request.FILES or None)
  if request.method == 'POST':
    if form.is_valid():
      # register new user
      profile = Profile(
        username=form.cleaned_data.get('login'),
        email=form.cleaned_data.get('email'),
        avatar=request.FILES.get('avatar')
      )
      profile.set_password(form.cleaned_data.get('password1'))
      profile.save()
      user = authenticate(request, username=form.cleaned_data.get('login'), password=form.cleaned_data.get('password1'))
      login(request, user)
      return redirect('index')
  context = {'form': form}
  context = add_tags_users_to_context(context)
  return render(request, 'qSite/signup.html', context)


def signout(request):
  logout(request)
  return redirect(request.META.get('HTTP_REFERER'))

def tag(request, tagName):
  questions = Tag.objects.by_tag_newest(tagName)
  page = paginate(request, questions, 20)
  context = {'questions': page.object_list, 'tag': tagName, 'page': page}
  context = add_tags_users_to_context(context)
  return render(request, 'qSite/tag.html', context)