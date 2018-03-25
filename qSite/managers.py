from django.db import models

class UserManager(models.Manager):

  def by_username(self, _username):
    return self.filter(user__username=_username)[0]
    # return self.get(user__username=_username)


class TagManager(models.Manager):

  def by_tag_newest(self, _tag):
    return self.filter(name=_tag)[0].questions.all().order_by('dateTime').reverse()
    # return self.get(name=_tag).questions.all().order_by('dateTime')


class LikeManager(models.Manager):
  pass


class QuestionManager(models.Manager):

  def newest(self):
    return self.order_by('dateTime').reverse()

  def hottest(self):
    return self.order_by('rating').reverse()

  def by_id(self, _id):
    return self.filter(pk=_id)[0]


class AnswerManager(models.Manager):
  
  def hottest(self, qid):
    return self.filter(question__id=qid).order_by('rating').reverse()