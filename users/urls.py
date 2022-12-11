from django.conf.urls import url
import views

urlpatterns = [
		
		url(r'^create-user/$', views.create_user, name='create_user'),
		url(r'^edit-user/(?P<pk>.*)/$', views.edit_user, name='edit_user'),
		url(r'^view-user/(?P<pk>.*)/$', views.view_user, name='view_user'),
		url(r'^view-users/$', views.view_users, name='view_users'),
		url(r'^verification/(?P<pk>.*)/$', views.verification, name='verification'),
		url(r'^activate/(?P<pk>.*)/$', views.activate, name='activate'),
		url(r'^terms/$', views.terms, name='terms'),
		url(r'^ruels/$', views.ruels, name='ruels'),

		url(r'^create-mail/(?P<pk>.*)/(?P<ad_id>.*)/$', views.create_mail, name='create_mail'),
		url(r'^sent-mail/$', views.sent_mail, name='sent_mail'),
		url(r'^received-mail/$', views.received_mail, name='received_mail'),
		url(r'^inbox-deleted/(?P<pk>.*)/$', views.inbox_deleted, name='inbox_deleted'),
		url(r'^sentitems_deleted/(?P<pk>.*)/$', views.sentitems_deleted, name='sentitems_deleted'),
	]