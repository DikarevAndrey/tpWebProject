from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from qSite.models import *


admin.site.register(Profile, UserAdmin)
admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(Answer)
admin.site.register(Like)