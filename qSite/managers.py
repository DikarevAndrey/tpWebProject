from django.db import models
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import UserManager as AbstractUserManager
# from django.db.models import Q

class UserManager(AbstractUserManager):

  def by_username(self, _username):
    return self.get(username=_username)
    # return get_object_or_404(self, username=_username)

  def by_id(self, _id):
    return get_object_or_404(self, pk=_id)

  def by_rating(self):
    return self.order_by('-rating')

  def search(self, _q):
    return self.filter(username__icontains=_q).order_by('-rating')


class TagManager(models.Manager):

  def by_tag_newest(self, _tag):
    return get_object_or_404(self, name=_tag).questions.all().order_by('-creationTime')

  def hottest(self):
    return self.annotate(question_count=Count('questions')).order_by('-question_count')

  def search(self, _q):
    return self.hottest().filter(name__icontains=_q)

class LikeManager(models.Manager):
  pass


class QuestionManager(models.Manager):

  def newest(self):
    return self.all()

  def hottest(self):
    return self.order_by('-rating')

  def by_id(self, _id):
    return get_object_or_404(self, pk=_id)

  def search(self, _q):
    return self.filter(tags__name__icontains=_q).order_by('-rating')
    # return self.filter(Q(title__icontains=q) | Q(text__icontains=q))

class AnswerManager(models.Manager):
  
  def hottest(self, qid):
    return self.filter(question__id=qid).order_by('-rating', '-creationTime')
