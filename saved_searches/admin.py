from django.contrib import admin
from saved_searches.models import SavedSearch


class SavedSearchAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('user_query', 'search_key', 'user', 'result_count', 'created')
    list_filter = ('search_key',)
    raw_id_fields = ('user',)
    search_fields = ('user_query', 'search_key')


admin.site.register(SavedSearch, SavedSearchAdmin)
