from django.contrib import admin
from django.contrib import admin
from .models import User, ResumeProfile, JobPost, Proposal, Message, MessageThread,ChatRoom

# Register your models here.

admin.site.register(User)
admin.site.register(ResumeProfile)
admin.site.register(JobPost)
admin.site.register(Proposal) 
admin.site.register(Message)
admin.site.register(MessageThread)
admin.site.register(ChatRoom)
