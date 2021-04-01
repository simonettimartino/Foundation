from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views #il punto indica la stessa directory
from django.conf.urls import url,include


urlpatterns = [
    #path('service_path', service_view, name="service_name"),
    url(r'^main/$', views.main, name='main'),
    # path('',views.homepage, name='homepage'),

]

urlpatterns = format_suffix_patterns(urlpatterns)