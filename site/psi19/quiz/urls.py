from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'quiz'
urlpatterns = [
    # /
    path('',                             views.home,                         name = 'home'),
    # /home
    path('home',                         views.home,                         name = 'home'),
    # /signup
    path('signup',                       views.signup,                       name = 'signup'),
    # /rank_list
    path('rank_list',                    views.global_rank_list,             name = 'rank_list'),
    # /search_results/
    url(r'^search_results/$',            views.search,                       name = 'search_results'),
    # /send_request/
    url(r'^send_request/(?P<value>\d+)/$',              views.send_request,                 name = 'send_request'),
    # /confirm_request
    url(r'^confirm_request/(?P<value>\d+)/$',           views.confirm_request,              name = 'confirm_request'),
    # /deny_request
    url(r'^deny_request/(?P<value>\d+)/$',              views.deny_request,                 name = 'deny_request'),
    # /cancel_request
    url(r'^cancel_request/(?P<value>\d+)/$',            views.cancel_request,               name = 'cancel_request'),
    # /unfriend
    url(r'^unfriend/(?P<value>\d+)/$',                  views.unfriend,                     name = 'unfriend'),
    # /submit_question
    url(r'^submit_question/$',           views.submit_a_question,            name = 'submit_a_question'),
    # /my_profile
    url(r'^my_profile/(?P<value>\d+)/$', views.my_profile,                   name = 'my_profile'),
    # /trophy_page
    url(r'^trophy_page/(?P<value>\d+)/$', views.trophy_page,                  name = 'trophy_page'),
    # /friends_page
    url(r'^friends_page/(?P<value>\d+)/$', views.friends_page,                 name = 'friends_page'),
    # /submit_wants_moderator
    url(r'^submit_wants_moderator/$',    views.submit_wants_moderator,       name = 'submit_wants_moderator'),
    # questions/need_validation
    url(r'^needs_validation/$',          views.needs_validation,             name = 'needs_validation'),
    # 
    url(r'^admin_question_overview/$',   views.admin_question_overview,      name = 'admin_question_overview'),
    
    url(r'^admin_remove_question/$',   views.admin_remove_question,      name = 'admin_remove_question'),
    
    # /approve_question
    url(r'^approve_question/$',          views.approve_question,             name = 'approve_question'),
    # /moderator_candidates
    url(r'^moderator_candidates/$',      views.moderator_candidates,         name = 'moderator_candidates'),
    # /approve_moderator
    url(r'^approve_moderator/$',         views.approve_moderator,            name = 'approve_moderator'),
    # /change_avatar
    url(r'^change_avatar/$',             views.change_avatar,                name = 'change_avatar'),
    # /choose_avatar
    url(r'^choose_avatar/$',             views.choose_avatar,                name = 'choose_avatar'),
    # /games_overview
    url(r'^games_overview/(?P<value>\d+)/$',             views.games_overview,                name = 'games_overview'),
    # /edit_question
    url(r'^edit_question/(?P<pk>\d+)/$',             views.edit_question,                name = 'edit_question'),


    # /report_form
    url(r'^report_form/$',             views.report_form,                name = 'report_form'),
    # /report_form_submit
    url(r'^report_form_submit/$',      views.report_form_submit,         name = 'report_form_submit'),
    # /report_list
    url(r'^report_list/$',             views.report_list,                name = 'report_list'),
    # /approve_report
    url(r'^approve_report/$',          views.approve_report,             name = 'approve_report'),


    # /create_game
    url(r'^create_game/$',          views.create_game,             name = 'create_game'),
    # /game
    url(r'^game/$',                 views.game,                    name = 'game'),
]