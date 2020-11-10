from django.contrib import admin
from .models import Organization, Cource, Topic, Schedule, UserCource

# Register your models here.

admin.site.register(Organization)
admin.site.register(Cource)
admin.site.register(Topic)
admin.site.register(Schedule)
admin.site.register(UserCource)