from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from random import randint
from django.core.paginator import Paginator


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
  else:
    tab = 'new'
  questions = []
  for i in range(1, 46):
    tags = []
    for j in range(1, 4):
      tags.append('tag' + str(i) + str(j))
    questions.append({
      'title': 'title ' + str(i),
      'id': i,
      'text': 'text' + str(i),
      'tags': tags,
      'likes': str(randint(0, 50)),
      'dislikes': str(randint(0, 50))
    })
  page = paginate(request, questions, 20)
  context = {'questions': page.object_list, 'tab': tab, 'page': page}
  return render(request, 'qSite/index.html', context)

def newQuestion(request):
  return render(request, 'qSite/ask.html')

def question(request, questionId):
  tags = []
  for i in range(1, 4):
    tags.append('tag' + str(i) + str(i))
  question = {
    'id': questionId,
    'title': 'title ' + str(questionId),
    'text': 'text' + str(questionId),
    'tags': tags,
    'likes': str(randint(0, 50)),
    'dislikes': str(randint(0, 50))
  }
  answers = []
  answers.append({
    'text': 'text' + str(1),
    'correct': 'true',
    'likes': str(20),
    'dislikes': str(4)
  })
  for i in range(2, 50):
    answers.append({
      'text': 'text' + str(i),
      'correct': 'false',
      'likes': str(randint(0, 50)),
      'dislikes': str(randint(0, 50))
    })

  page = paginate(request, answers, 30)
  context = {'question': question, 'answers': page.object_list, 'page': page}
  return render(request, 'qSite/question.html', context)

def signin(request):
  return render(request, 'qSite/login.html')

def signup(request):
  return render(request, 'qSite/signup.html')

def tag(request, tagName):
  questions = []
  for i in range(1, 46):
    tags = []
    for j in range(1, 3):
      tags.append('tag' + str(i) + str(j))
    tags.append(tagName)
    questions.append({
      'title': 'title ' + str(i),
      'id': i,
      'text': 'text' + str(i),
      'tags': tags,
      'likes': str(randint(0, 50)),
      'dislikes': str(randint(0, 50))
    })

  page = paginate(request, questions, 20)
  context = {'questions': page.object_list, 'tag': tagName, 'page': page}
  return render(request, 'qSite/tag.html', context)