import datetime
from django.contrib.auth.models import User
from django.db import models


class SavedSearch(models.Model):
    search_key = models.SlugField(max_length=100, help_text="A way to arbitrarily group queries. Should be a single word. Example: all-products")
    user_query = models.CharField(max_length=1000, help_text="The text the user searched on. Useful for display.")
    full_query = models.CharField(max_length=1000, help_text="The full query Haystack generated. Useful for searching again.")
    result_count = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, blank=True, null=True, related_name='saved_searches')
    created = models.DateTimeField(default=datetime.datetime.now)
    
    def __unicode__(self):
        if self.user:
            return u"'%s...' by %s:%s" % (self.user_query[:50], self.user.username, self.search_key)
        
        return u"'%s...' by Anonymous:%s" % (self.user_query[:50], self.search_key)
