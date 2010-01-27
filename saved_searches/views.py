from haystack.views import SearchView
from saved_searches.models import SavedSearch


class SavedSearchView(SearchView):
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
        
        saved_search = SavedSearch(
            search_key=self.search_key,
            user_query=self.query,
            result_count=paginator.count
        )
        
        query_seen = self.searchqueryset.query.build_query()
        
        if isinstance(query_seen, basestring):
            saved_search.full_query = query_seen
        
        if request.user.is_authenticated():
            saved_search.user = request.user
        
        saved_search.save()
        
        context = {
            'query': self.query,
            'form': self.form,
            'page': page,
            'paginator': paginator,
        }
        context.update(self.extra_context())
        
        return render_to_response(self.template, context, context_instance=self.context_class(self.request))
