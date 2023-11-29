from django.contrib import admin

# Register your models here.
from .models import LiveEvent, UserEventStatus, Profile

#admin.site.register(LiveEvent)
#admin.site.register(UserEventStatus)

admin.site.register(Profile)

admin.site.register(LiveEvent)
