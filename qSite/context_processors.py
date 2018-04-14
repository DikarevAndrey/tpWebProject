from qSite.models import Profile, Tag
def add_tags_users_to_context(request):
  top_users = Profile.objects.by_rating()[:3]
  top_tags = Tag.objects.hottest()[:3]
  return {'top_users': top_users, 'top_tags': top_tags}