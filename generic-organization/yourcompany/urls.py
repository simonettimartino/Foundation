from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views #il punto indica la stessa directory
from django.conf.urls import url,include
from . import views #il punto indica la stessa directory

from django.urls import include, path, re_path


urlpatterns = [
    #path('service_path', service_view, name="service_name"),
    #url(r'^main/$', views.main, name='main'),
    #path(r'^account_profile/$', views.account_profile, name='account_profile')
    # path('',views.homepage, name='homepage'),

]

urlpatterns2 = format_suffix_patterns(urlpatterns)