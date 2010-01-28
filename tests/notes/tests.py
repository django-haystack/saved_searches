from django.contrib.auth.models import User
from django.test import TestCase
from saved_searches.models import SavedSearch
from notes.models import Note


class SavedSearchTestCase(TestCase):
    def setUp(self):
        super(SavedSearchTestCase, self).setUp()
        self.user1 = User.objects.create_user('testy', 'test@example.com', 'test')
        # self.user1.is_active = True
        # self.user1.save()
        self.note1 = Note.objects.create(
            title='A test note',
            content='Because everyone loves test data.',
            author='Daniel'
        )
        self.note2 = Note.objects.create(
            title='Another test note',
            content='Something to test with.',
            author='John'
        )
        self.note3 = Note.objects.create(
            title='NEVER GOING TO GIVE YOU UP',
            content='NEVER GOING TO LET YOU DOWN.',
            author='Rick'
        )
    
    def test_usage(self):
        # Check the stat pages first.
        resp = self.client.get('/search_stats/most_recent/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['by_user'], None)
        self.assertEqual(resp.context['by_search_key'], None)
        self.assertEqual(len(resp.context['page'].object_list), 0)
        self.assertEqual(resp.context['paginator'].num_pages, 1)
        
        resp = self.client.get('/search_stats/most_popular/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['by_user'], None)
        self.assertEqual(resp.context['by_search_key'], None)
        self.assertEqual(len(resp.context['page'].object_list), 0)
        self.assertEqual(resp.context['paginator'].num_pages, 1)
        
        
        # Sanity check.
        resp = self.client.get('/search/')
        self.assertEqual(resp.status_code, 200)
        
        # Run a couple searches.
        resp = self.client.get('/search/', data={'q': 'test'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['page'].object_list), 2)
        self.assertEqual(SavedSearch.objects.all().count(), 1)
        
        resp = self.client.get('/search/', data={'q': 'everyone'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['page'].object_list), 1)
        self.assertEqual(SavedSearch.objects.all().count(), 2)
        
        resp = self.client.get('/search/', data={'q': 'test data'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['page'].object_list), 1)
        self.assertEqual(SavedSearch.objects.all().count(), 3)
        
        resp = self.client.get('/search/', data={'q': 'test'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['page'].object_list), 2)
        self.assertEqual(SavedSearch.objects.all().count(), 4)
        
        # Run a couple user searches.
        self.assertEqual(self.client.login(username='testy', password='test'), True)
        
        resp = self.client.get('/search/', data={'q': 'test'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['page'].object_list), 2)
        self.assertEqual(SavedSearch.objects.all().count(), 5)
        self.assertEqual(SavedSearch.objects.filter(user=self.user1).count(), 1)
        
        resp = self.client.get('/search/', data={'q': 'everyone'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['page'].object_list), 1)
        self.assertEqual(SavedSearch.objects.all().count(), 6)
        self.assertEqual(SavedSearch.objects.filter(user=self.user1).count(), 2)
        
        resp = self.client.get('/search/', data={'q': 'test'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['page'].object_list), 2)
        self.assertEqual(SavedSearch.objects.all().count(), 7)
        self.assertEqual(SavedSearch.objects.filter(user=self.user1).count(), 3)
        
        self.client.logout()
        
        
        # Check to see if stats updated.
        resp = self.client.get('/search_stats/most_recent/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['by_user'], None)
        self.assertEqual(resp.context['by_search_key'], None)
        self.assertEqual([ss['user_query'] for ss in resp.context['page'].object_list], [u'test', u'everyone', u'test', u'test', u'test data', u'everyone', u'test'])
        self.assertEqual(resp.context['paginator'].num_pages, 1)
        
        resp = self.client.get('/search_stats/most_recent/username/testy/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['by_user'].username, 'testy')
        self.assertEqual(resp.context['by_search_key'], None)
        self.assertEqual([ss['user_query'] for ss in resp.context['page'].object_list], [u'test', u'everyone', u'test'])
        self.assertEqual(resp.context['paginator'].num_pages, 1)
        
        resp = self.client.get('/search_stats/most_recent/area/general/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['by_user'], None)
        self.assertEqual(resp.context['by_search_key'], u'general')
        self.assertEqual([ss['user_query'] for ss in resp.context['page'].object_list], [u'test', u'everyone', u'test', u'test', u'test data', u'everyone', u'test'])
        self.assertEqual(resp.context['paginator'].num_pages, 1)
        
        resp = self.client.get('/search_stats/most_popular/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['by_user'], None)
        self.assertEqual(resp.context['by_search_key'], None)
        self.assertEqual([ss['user_query'] for ss in resp.context['page'].object_list], [u'test', u'everyone', u'test data'])
        self.assertEqual([ss['times_seen'] for ss in resp.context['page'].object_list], [4, 2, 1])
        self.assertEqual(resp.context['paginator'].num_pages, 1)
        
        resp = self.client.get('/search_stats/most_popular/username/testy/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['by_user'].username, 'testy')
        self.assertEqual(resp.context['by_search_key'], None)
        self.assertEqual([ss['user_query'] for ss in resp.context['page'].object_list], [u'test', u'everyone'])
        self.assertEqual([ss['times_seen'] for ss in resp.context['page'].object_list], [2, 1])
        self.assertEqual(resp.context['paginator'].num_pages, 1)
        
        resp = self.client.get('/search_stats/most_popular/area/general/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['by_user'], None)
        self.assertEqual(resp.context['by_search_key'], u'general')
        self.assertEqual([ss['user_query'] for ss in resp.context['page'].object_list], [u'test', u'everyone', u'test data'])
        self.assertEqual([ss['times_seen'] for ss in resp.context['page'].object_list], [4, 2, 1])
        self.assertEqual(resp.context['paginator'].num_pages, 1)
