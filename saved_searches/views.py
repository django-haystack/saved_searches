import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from haystack.views import SearchView
from saved_searches.models import SavedSearch


SAVED_SEARCHES_PER_PAGE = getattr(settings, 'SAVED_SEARCHES_PER_PAGE', 50)


class SavedSearchView(SearchView):
    """
    Automatically handles saving the queries when they are run.
    """
    search_key = 'general'
    
    def __init__(self, *args, **kwargs):
        if 'search_key' in kwargs:
            self.search_key = kwargs['search_key']
            del(kwargs['search_key'])
        
        super(SavedSearchView, self).__init__(*args, **kwargs)
    
    def create_response(self):
        """
        Saves the details of a user's search and then generates the actual
        HttpResponse to send back to the user.
        """
        (paginator, page) = self.build_page()
        
        # Only save the search if we're on the first page.
        # This will prevent an excessive number of duplicates for what is
        # essentially the same search.
        if self.query and page.number == 1:
            # Save the search.
            saved_search = SavedSearch(
                search_key=self.search_key,
                user_query=self.query,
                result_count=len(self.results)
            )
            
            if hasattr(self.results, 'query'):
                query_seen = self.results.query.build_query()
            
                if isinstance(query_seen, basestring):
                    saved_search.full_query = query_seen
            
            if self.request.user.is_authenticated():
                saved_search.user = self.request.user
            
            saved_search.save()
        
        context = {
            'query': self.query,
            'form': self.form,
            'page': page,
            'paginator': paginator,
        }
        context.update(self.extra_context())
        
        return render_to_response(self.template, context, context_instance=self.context_class(self.request))


def most_recent(request, username=None, search_key=None):
    """
    Shows the most recent search results.
    
    The ``username`` kwarg should be the ``username`` field of
    ``django.contrib.auth.models.User``. The ``search_key`` can be any string.
    
    Template::
        ``saved_searches/most_recent.html``
    Context::
        ``by_user``
            The ``User`` object corresponding to the username, if provided.
        ``by_search_key``
            The search_key, if provided.
        ``page``
            The request page of recent results (a dict of ``user_query`` + ``created``).
        ``paginator``
            The paginator object for the full result set.
    """
    if username is not None:
        user = get_object_or_404(User, username=username)
    else:
        user = None
    
    most_recent = SavedSearch.objects.most_recent(user=user, search_key=search_key)
    paginator = Paginator(most_recent, SAVED_SEARCHES_PER_PAGE)
    
    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404("Invalid page.")
    
    return render_to_response('saved_searches/most_recent.html', {
        'by_user': user,
        'by_search_key': search_key,
        'page': page,
        'paginator': paginator,
    }, context_instance=RequestContext(request))


def most_popular(request, username=None, search_key=None):
    """
    Shows the most popular search results.
    
    The ``username`` kwarg should be the ``username`` field of
    ``django.contrib.auth.models.User``. The ``search_key`` can be any string.
    
    Template::
        ``saved_searches/most_popular.html``
    Context::
        ``by_user``
            The ``User`` object corresponding to the username, if provided.
        ``by_search_key``
            The search_key, if provided.
        ``page``
            The request page of popular results (a dict of ``user_query`` + ``times_seen``).
        ``paginator``
            The paginator object for the full result set.
    """
    if username is not None:
        user = get_object_or_404(User, username=username)
    else:
        user = None
    
    most_recent = SavedSearch.objects.most_popular(user=user, search_key=search_key)
    paginator = Paginator(most_recent, SAVED_SEARCHES_PER_PAGE)
    
    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404("Invalid page.")
    
    return render_to_response('saved_searches/most_popular.html', {
        'by_user': user,
        'by_search_key': search_key,
        'page': page,
        'paginator': paginator,
    }, context_instance=RequestContext(request))
    