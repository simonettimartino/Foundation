from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url,include
from . import views #il punto indica la stessa directory

from django.urls import include, path, re_path


urlpatterns = [
    #path('service_path', service_view, name="service_name"),
    #url(r'^test/$', views.test, name='test'),
    #path(r'^account_profile/$', views.account_profile, name='account_profile')
    #path('',views.test, name='test'),

]

urlpatterns2 = format_suffix_patterns(urlpatterns)