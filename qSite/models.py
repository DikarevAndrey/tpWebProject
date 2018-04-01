from django.db import models
from django.utils import timezone
from qSite.managers import *
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Profile(AbstractUser):
  avatar = models.ImageField(
    default="../img/nobody.jpg",
    upload_to='uploads/%Y/%m/%d/',
    verbose_name="Avatar image of the user"
  )
  rating = models.IntegerField(default=0, verbose_name="Rating of the user")

  objects = UserManager()

  def __str__(self):
    return self.username


class Tag(models.Model):
  name = models.CharField(max_length=15, verbose_name="Name of the tag")

  objects = TagManager()

  def __str__(self):
    return self.name

  class Meta:
    ordering = ['name']


class Like(models.Model):
  LIKE = 1
  DISLIKE = -1
  VALUES = ((DISLIKE, 'DISLIKE'), (LIKE, 'LIKE'),)
  author = models.ForeignKey(
    Profile,
    null=False,
    verbose_name="Author of the vote",
    on_delete=models.CASCADE
  )
  value = models.IntegerField(
    choices=VALUES,
    verbose_name="Like or dislike",
    null=False
  )

  content_type = models.ForeignKey(
    ContentType,
    on_delete=models.CASCADE,
    null=True
  )
  object_id = models.PositiveIntegerField(
    null=True,
    verbose_name="id of related object"
  )
  content_object = GenericForeignKey('content_type', 'object_id')

  objects = LikeManager()

  def __str__(self):
    return str(self.value) + ' from ' + self.author.username

  class Meta:
    unique_together = ('author', 'content_type', 'object_id',)


class Question(models.Model):
  author = models.ForeignKey(
    Profile,
    null=False,
    verbose_name="Author of the question",
    on_delete=models.CASCADE
  )

  title = models.CharField(
    max_length=100,
    verbose_name="Title of the question"
  )
  text = models.TextField(verbose_name="Full text of the question")
  tags = models.ManyToManyField(
    Tag,
    blank=True,
    verbose_name="Tags of the question",
    related_name='questions'
  )
  creationTime = models.DateTimeField(
    default=timezone.now,
    verbose_name="Date and time the question was published"
  )

  likes = GenericRelation(Like, related_query_name='questions')
  rating = models.IntegerField(default=0, verbose_name="Votes ratio")

  objects = QuestionManager()

  def update_rating(self):
    like_count = self.likes.filter(value=1).count()
    dislike_count = self.likes.filter(value=-1).count()
    self.rating = like_count - dislike_count
    self.save()

  def __str__(self):
    return self.text

  class Meta:
    ordering = ['-creationTime']


class Answer(models.Model):
  author = models.ForeignKey(
    Profile,
    null=False,
    verbose_name="Author of the answer",
    on_delete=models.CASCADE
  )
  question = models.ForeignKey(
    Question,
    null=False,
    on_delete=models.CASCADE,
    verbose_name="Question that is being answered"
  )

  text = models.TextField(verbose_name="Full text of the answer")
  creationTime = models.DateTimeField(
    default=timezone.now,
    verbose_name="Date and time the answer was published"
  )

  likes = GenericRelation(Like, related_query_name='answers')
  rating = models.IntegerField(default=0, verbose_name="Votes ratio")
  is_correct = models.BooleanField(
    default=False,
    verbose_name="If answer is marked as correct"
  )

  objects = AnswerManager()

  def update_rating(self):
    like_count = self.likes.filter(value=1).count()
    dislike_count = self.likes.filter(value=-1).count()
    self.rating = like_count - dislike_count
    self.save()

  def __str__(self):
    return self.text

  class Meta:
    ordering = ['-creationTime']


@receiver(post_save, sender=Like)
def update_related_rating(sender, instance, **kwargs):
  instance.content_object.update_rating()

@receiver(post_delete, sender=Like)
def update_related_rating(sender, instance, **kwargs):
  instance.content_object.update_rating()