from django.contrib import admin

# Register your models here.
from comment_handle.models import Comment

admin.site.register(Comment)