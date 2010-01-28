from django.conf.urls.defaults import *
from saved_searches.views import SavedSearchView


urlpatterns = patterns('',
    url(r'^search/$', SavedSearchView(), name='search'),
    url(r'^search_stats/', include('saved_searches.urls')),
)
