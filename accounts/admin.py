from django.contrib import admin
from accounts.models import UserProfile, Post

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Post)
#admin.site.site_header='Administration'
