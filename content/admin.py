from django.contrib import admin
from .models import Tag, Content, Shortform, Message


admin.site.register(Tag)
admin.site.register(Content)
admin.site.register(Shortform)
admin.site.register(Message)