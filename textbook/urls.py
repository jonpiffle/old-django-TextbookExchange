from django.conf.urls import patterns, include, url
from . import views
from django.contrib import admin
from message.forms import CustomRegistrationForm
from .views import CustomRegistrationView

admin.autodiscover()

urlpatterns = patterns('',
     url(r'^$', views.HomepageView.as_view(), name="home"),
     url(r'', include("exchange.urls", namespace="exchange")),
     url(r'', include("message.urls", namespace="message")),
     url(r'^accounts/register/$', CustomRegistrationView.as_view(form_class = CustomRegistrationForm), name='registration_register'),
     url(r'^accounts/', include('registration.backends.simple.urls')),
     url(r'^admin/', include(admin.site.urls)),
		
)
