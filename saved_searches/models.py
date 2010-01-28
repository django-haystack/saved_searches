import datetime
from django.contrib.auth.models import User
from django.db import models


class SavedSearchManager(models.Manager):
    def most_recent(self, user=None, search_key=None):
        """
        Returns the most recently seen queries.
        
        Can filter by ``user`` and/or ``search_key`` if provided.
        """
        qs = self.get_query_set()
        
        if user is not None:
            qs = qs.filter(user=user)
        
        if search_key is not None:
            qs = qs.filter(search_key=search_key)
        
        return qs.values('user_query', 'created').order_by('-created')
    
    def most_popular(self, user=None, search_key=None):
        """
        Returns the most popular (frequently seen) queries.
        
        Can filter by ``user`` and/or ``search_key`` if provided.
        """
        qs = self.get_query_set()
        
        if user is not None:
            qs = qs.filter(user=user)
        
        if search_key is not None:
            qs = qs.filter(search_key=search_key)
        
        return qs.values('user_query').order_by().annotate(times_seen=models.Count('user_query')).order_by('-times_seen')


class SavedSearch(models.Model):
    search_key = models.SlugField(max_length=100, help_text="A way to arbitrarily group queries. Should be a single word. Example: all-products")
    user_query = models.CharField(max_length=1000, help_text="The text the user searched on. Useful for display.")
    full_query = models.CharField(max_length=1000, default='', blank=True, help_text="The full query Haystack generated. Useful for searching again.")
    result_count = models.PositiveIntegerField(default=0, blank=True)
    user = models.ForeignKey(User, blank=True, null=True, related_name='saved_searches')
    created = models.DateTimeField(blank=True, default=datetime.datetime.now)
    
    objects = SavedSearchManager()
    
    def __unicode__(self):
        if self.user:
            return u"'%s...' by %s:%s" % (self.user_query[:50], self.user.username, self.search_key)
        
        return u"'%s...' by Anonymous:%s" % (self.user_query[:50], self.search_key)
