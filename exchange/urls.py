from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('',
       url (
           regex = '^textbooks/list/$',
           view =  TextbookListView.as_view(),
           name = 'textbook_list'
       ),
 
       url (
           regex = '^textbooks/detail/(?P<pk>\d+)/$',
           view =  TextbookDetailView.as_view(),
           name = 'textbook_detail'
       ),
       url (
           regex = '^textbooks/create/$',
           view =  TextbookCreateView.as_view(),
           name = 'textbook_create'
       ),
 
       url (
           regex = '^textbooks/delete/(?P<pk>\d+)/$',
           view =  TextbookDeleteView.as_view(),
           name = 'textbook_delete'
       ),
       url (
           regex = '^textbooks/update/(?P<pk>\d+)/$',
           view =  TextbookUpdateView.as_view(),
           name = 'textbook_update'
       ),
			 url (
           regex = '^library/$',
           view =  OwnListView.as_view(),
           name = 'library'
       ),
			 url (
           regex = '^owns/update/(?P<pk>\d+)/$',
           view =  OwnUpdateView.as_view(),
           name = 'own_update'
       ),
       url (
           regex = '^owns/create/$',
           view =  OwnCreateView.as_view(),
           name = 'own_create'
       ),
       url (
           regex = '^owns/delete/(?P<pk>\d+)/$',
           view =  OwnDeleteView.as_view(),
           name = 'own_delete'
       ),
       url (
           regex = '^selling/list/$',
           view =  SellingListView.as_view(),
           name = 'selling_list'
       ),
)
