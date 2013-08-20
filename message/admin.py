from django.contrib import admin
from message.models import Person, Message, Conversation, Notification

admin.site.register(Person)
admin.site.register(Message)
admin.site.register(Conversation)
admin.site.register(Notification)