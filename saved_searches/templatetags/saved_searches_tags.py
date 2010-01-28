from django import template
from saved_searches.models import SavedSearch


register = template.Library()


class MostRecentNode(template.Node):
    def __init__(self, varname, user=None, search_key=None, limit=10):
        self.varname = varname
        self.user = user
        self.search_key = search_key
        self.limit = int(limit)
    
    def render(self, context):
        user = None
        search_key = None
        
        if self.user is not None:
            temp_user = template.Variable(self.user)
            user = temp_user.resolve(context)
        
        if self.search_key is not None:
            temp_search_key = template.Variable(self.search_key)
            search_key = temp_search_key.resolve(context)
        
        context[self.varname] = SavedSearch.objects.most_recent(user=user, search_key=search_key)[:self.limit]
        return ''


@register.tag
def most_recent_searches(parser, token):
    """
    Returns the most recent queries seen. By default, returns the top 10.
    
    Usage::
    
        {% most_recent_searches as <varname> [for_user user] [for_search_key search_key] [limit n] %}
    
    Example::
    
        {% most_recent_searches as recent %}
        {% most_recent_searches as recent for_user request.user %}
        {% most_recent_searches as recent for_search_key "general" %}
        {% most_recent_searches as recent limit 5 %}
        {% most_recent_searches as recent for_user request.user for_search_key "general" limit 15 %}
    """
    bits = token.split_contents()
    tagname = bits[0]
    bits = bits[1:]
    
    if len(bits) < 2:
        raise template.TemplateSyntaxError("%r tag requires at least two arguments." % tagname)
    
    varname = bits[1]
    bits = iter(bits[2:])
    user = None
    search_key = None
    limit = 10
    
    for bit in bits:
        if bit == 'for_user':
            user = bits.next()
        if bit == 'for_search_key':
            search_key = bits.next()
        if bit == 'limit':
            limit = bits.next()
    
    return MostRecentNode(varname, user, search_key, limit)


class MostPopularNode(template.Node):
    def __init__(self, varname, user=None, search_key=None, limit=10):
        self.varname = varname
        self.user = user
        self.search_key = search_key
        self.limit = int(limit)
    
    def render(self, context):
        user = None
        search_key = None
        
        if self.user is not None:
            temp_user = template.Variable(self.user)
            user = temp_user.resolve(context)
        
        if self.search_key is not None:
            temp_search_key = template.Variable(self.search_key)
            search_key = temp_search_key.resolve(context)
        
        context[self.varname] = SavedSearch.objects.most_popular(user=user, search_key=search_key)[:self.limit]
        return ''


@register.tag
def most_popular_searches(parser, token):
    """
    Returns the most popular queries seen. By default, returns the top 10.
    
    Usage::
    
        {% most_popular_searches as <varname> [for_user user] [for_search_key search_key] [limit n] %}
    
    Example::
    
        {% most_popular_searches as popular %}
        {% most_popular_searches as popular for_user request.user %}
        {% most_popular_searches as popular for_search_key "general" %}
        {% most_popular_searches as popular limit 5 %}
        {% most_popular_searches as popular for_user request.user for_search_key "general" limit 15 %}
    """
    bits = token.split_contents()
    tagname = bits[0]
    bits = bits[1:]
    
    if len(bits) < 2:
        raise template.TemplateSyntaxError("%r tag requires at least two arguments." % tagname)
    
    varname = bits[1]
    bits = iter(bits[2:])
    user = None
    search_key = None
    limit = 10
    
    for bit in bits:
        if bit == 'for_user':
            user = bits.next()
        if bit == 'for_search_key':
            search_key = bits.next()
        if bit == 'limit':
            limit = bits.next()
    
    return MostPopularNode(varname, user, search_key, limit)
