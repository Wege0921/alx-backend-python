from django.contrib import admin
from .models import Message

class ReplyInline(admin.TabularInline):
    model = Message
    fk_name = 'parent_message'
    extra = 0
    show_change_link = True

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'content', 'parent_message', 'timestamp')
    inlines = [ReplyInline]

admin.site.register(Message, MessageAdmin)
