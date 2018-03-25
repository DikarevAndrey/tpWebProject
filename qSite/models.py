from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from qSite.managers import *

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Basic user info")
  avatar = models.ImageField(default="img/nobody.jpg", upload_to='uploads/%Y/%m/%d/', verbose_name="Avatar image of the user")
  rating = models.IntegerField(default=0, verbose_name="Rating of the user")

  objects = UserManager()

  def __str__(self):
    return self.user.username


class Tag(models.Model):
  name = models.CharField(max_length=15, verbose_name="Name of the tag")

  objects = TagManager()

  def __str__(self):
    return self.name

  class Meta:
    ordering = ['name']


class Like(models.Model):
  VALUES = ((-1, 'DISLIKE'), (1, 'LIKE'))
  author = models.ForeignKey(Profile, null=False, verbose_name="Author of the vote", on_delete=models.DO_NOTHING)
  value = models.IntegerField(choices=VALUES, verbose_name="Like or dislike", null=False)

  objects = LikeManager()

  def __str__(self):
    return value + ' from ' + author.user.username


class Question(models.Model):
  title = models.CharField(max_length=100, verbose_name="Title of the question")
  text = models.TextField(verbose_name="Full text of the question")
  dateTime = models.DateTimeField(default=timezone.now, verbose_name="Date and time the question was published")
  author = models.ForeignKey(Profile, null=False, verbose_name="Author of the question", on_delete=models.DO_NOTHING)
  tags = models.ManyToManyField(Tag, blank=True, verbose_name="Tags of the question", related_name='questions')
  likes = models.ManyToManyField(Like, blank=True, verbose_name="Likes of the question", related_name='questions')
  rating = models.IntegerField(default=0, verbose_name="Votes ratio")

  objects = QuestionManager()

  def __str__(self):
    return self.text

  class Meta:
    ordering = ['-dateTime']


class Answer(models.Model):
  question = models.ForeignKey(Question, null=False, on_delete=models.CASCADE, verbose_name="Question that is being answered")
  text = models.TextField(verbose_name="Full text of the answer")
  author = models.ForeignKey(Profile, null=False, verbose_name="Author of the answer", on_delete=models.DO_NOTHING)
  dateTime = models.DateTimeField(default=timezone.now, verbose_name="Date and time the answer was published")
  likes = models.ManyToManyField(Like, blank=True, verbose_name="Likes of the question")
  rating = models.IntegerField(default=0, verbose_name="Votes ratio")
  correct = models.BooleanField(default=False, verbose_name="If answer is marked as correct")

  objects = AnswerManager()

  def __str__(self):
    return self.text

  class Meta:
    ordering = ['-dateTime']