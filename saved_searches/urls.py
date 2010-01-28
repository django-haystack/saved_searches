from django.conf.urls.defaults import *


urlpatterns = patterns('saved_searches.views',
    url(r'^most_recent/$', 'most_recent', name='saved_searches_most_recent'),
    url(r'^most_recent/username/(?P<username>[\w\d._-]+)/$', 'most_recent', name='saved_searches_most_recent_by_user'),
    url(r'^most_recent/area/(?P<search_key>[\w\d._-]*)/$', 'most_recent', name='saved_searches_most_recent_by_search_key'),
    url(r'^most_recent/area/(?P<search_key>[\w\d._-]*)/username/(?P<username>[\w\d._-]+)/$', 'most_recent', name='saved_searches_most_recent_by_user_search_key'),
    
    url(r'^most_popular/$', 'most_popular', name='saved_searches_most_popular'),
    url(r'^most_popular/username/(?P<username>[\w\d._-]+)/$', 'most_popular', name='saved_searches_most_popular_by_user'),
    url(r'^most_popular/area/(?P<search_key>[\w\d._-]*)/$', 'most_popular', name='saved_searches_most_popular_by_search_key'),
    url(r'^most_popular/area/(?P<search_key>[\w\d._-]*)/username/(?P<username>[\w\d._-]+)/$', 'most_popular', name='saved_searches_most_popular_by_user_search_key'),
)
