from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'quiz'
urlpatterns = [
    path('',                             views.home,                         name = 'home'),
    path('home',                         views.home,                         name = 'home'),
    path('signup',                       views.signup,                       name = 'signup'),
    path('rank_list',                    views.global_rank_list,             name = 'rank_list'),
    url(r'^search_results/$',            views.search,                       name = 'search_results'),
    url(r'^send_request/$',              views.send_request,                 name = 'send_request'),
    url(r'^confirm_request/$',           views.confirm_request,              name = 'confirm_request'),
    url(r'^cancel_request/$',            views.cancel_request,               name = 'cancel_request'),
    url(r'^unfriend/$',                  views.unfriend,                     name = 'unfriend'),
    url(r'^submit_question/$',           views.submit_a_question,            name = 'submit_a_question'),
    
    # questions/need_validation
    url(r'^needs_validation/$',  views.needs_validation,             name = 'needs_validation'),

    # questions/2/update
    url(r'^questions/(?P<pk>\d+)/update/$',    views.EditQuestion.as_view(), name = 'update-question'),
]