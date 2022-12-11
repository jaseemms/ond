from django.conf.urls import url
import views

urlpatterns = [
		url(r'^$', views.view_advertisements, name='view_advertisements'),
		url(r'^my-advertisements$', views.my_advertisements, name='my_advertisements'),
		url(r'^create-advertisement/$', views.create_advertisement, name='create_advertisement'),
		url(r'^edit-advertisement/(?P<pk>.*)/$', views.edit_advertisement, name='edit_advertisement'),
		url(r'^view-advertisement/(?P<pk>.*)/$', views.view_advertisement, name='view_advertisement'),
		url(r'^delete-advertisement/(?P<pk>.*)/$', views.delete_advertisement, name='delete_advertisement'),
		url(r'^ad-activate/(?P<pk>.*)/$', views.ad_activate, name='ad_activate'),
		url(r'^premium/(?P<pk>.*)/$', views.premium, name='premium'),
		url(r'^get-ajax/$', views.get_ajax, name='get_ajax')
	]