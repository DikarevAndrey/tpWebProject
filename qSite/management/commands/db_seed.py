from django.core.management.base import BaseCommand
from qSite.models import *
from faker import Faker
import random

class Command(BaseCommand):
  help = 'Seeds database with test data'

  USERS_COUNT = 20
  TAGS_COUNT = 100
  MAX_QUESTIONS_PER_USER = 20
  MAX_ANSWERS_PER_QUESTION = 100


  def handle(self, *args, **options):
    users = self.generate_users()
    tags = self.generate_tags()
    questions = self.generate_questions(users=users, tags=tags)
    self.generate_answers(questions=questions, users=users)
    self.stdout.write(self.style.SUCCESS('Successfully generated data.'))


  def generate_users(self):
    Profile.objects.all().delete()
    list_of_users = []

    fake = Faker()
    for i in range(0, self.USERS_COUNT):
      username = fake.simple_profile().get("username") + str(i)
      user = Profile.objects.create_user(username=username, password=username)
      user.first_name = fake.first_name()
      user.last_name = fake.last_name()
      user.rating = random.randint(-50, 50)
      user.save()

      list_of_users.append(user)

    self.stdout.write(self.style.SUCCESS('Successfully generated users.'))
    return list_of_users


  def generate_tags(self):
    Tag.objects.all().delete()
    list_of_tags = []

    fake = Faker()
    for i in range(0, self.TAGS_COUNT):
      name = fake.word() + str(i)
      tag = Tag(name=name)
      tag.save()
      list_of_tags.append(tag)

    self.stdout.write(self.style.SUCCESS('Successfully generated tags.'))
    return list_of_tags


  def generate_questions(self, users, tags):
    Question.objects.all().delete()
    list_of_questions = []

    fake = Faker()
    for user in users:
      for i in range(0, random.randint(0, self.MAX_QUESTIONS_PER_USER)):
        title = fake.sentence(nb_words=8)
        text = fake.text()
        creationTime = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
        author = user
        rating = random.randint(-50, 50)
        question = Question(title=title, text=text, creationTime=creationTime, author=author, rating=rating)
        question.save()
        for i in range(0, 3):
          tag = random.choice(tags)
          question.tags.add(tag)
        question.save()
        list_of_questions.append(question)

    self.stdout.write(self.style.SUCCESS('Successfully generated questions.'))
    return list_of_questions


  def generate_answers(self, questions, users):
    Answer.objects.all().delete()

    fake = Faker()
    for question in questions:
      for i in range(0, random.randint(0, self.MAX_ANSWERS_PER_QUESTION)):
        user = random.choice(users)
        text = fake.text()
        creationTime = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
        rating = random.randint(-50, 50)
        answer = Answer(text=text, creationTime=creationTime, author=user, question=question, rating=rating)
        answer.save()

    self.stdout.write(self.style.SUCCESS('Successfully generated answers.'))