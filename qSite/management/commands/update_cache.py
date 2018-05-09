from django.core.management.base import BaseCommand
from django.core.cache import cache
from qSite.models import Profile, Tag


class Command(BaseCommand):
  help = 'Update django cache'

  def handle(self, *args, **options):
    top_users = Profile.objects.by_rating()[:3]
    top_tags = Tag.objects.hottest()[:3]
    cache.set_many({'top_users': top_users, 'top_tags': top_tags})