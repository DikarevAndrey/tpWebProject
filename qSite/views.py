from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from random import randint
from django.core.paginator import Paginator, EmptyPage
from qSite.models import *

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


def newQuestion(request):
  context = add_tags_users_to_context({})
  return render(request, 'qSite/ask.html', context)


def question(request, questionId):
  question = Question.objects.by_id(questionId)
  answers = Answer.objects.hottest(questionId)
  page = paginate(request, answers, 30)
  context = {'question': question, 'answers': page.object_list, 'page': page, 'answers_count': answers.count()}
  context = add_tags_users_to_context(context)
  return render(request, 'qSite/question.html', context)


def signin(request):
  context = add_tags_users_to_context({})
  return render(request, 'qSite/login.html', context)


def signup(request):
  context = add_tags_users_to_context({})
  return render(request, 'qSite/signup.html', context)


def tag(request, tagName):
  questions = Tag.objects.by_tag_newest(tagName)
  page = paginate(request, questions, 20)
  context = {'questions': page.object_list, 'tag': tagName, 'page': page}
  context = add_tags_users_to_context(context)
  return render(request, 'qSite/tag.html', context)