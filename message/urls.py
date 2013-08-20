from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('',
      url (
           regex = '^conversations/$',
           view =  ConversationListView.as_view(),
           name = 'conversation_list'
      ),
      url (
           regex = '^messages/create/$',
           view =  MessageCreateView.as_view(),
           name = 'message_create'
      ),
      url (
           regex = '^conversations/detail/(?P<pk>\d+)/$',
           view =  ConversationDetailView.as_view(),
           name = 'conversation_detail'
      ),
      url (
           regex = '^conversations/router/',
           view =  conversation_router,
           name = 'conversation_router'
      ),
)