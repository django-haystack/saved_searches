=============
saved_searches
=============

Allows you to personalize search by storing a user's search history.

For use with Haystack (http://haystacksearch.org/).


Requirements
============

* Django 1.1+ (May work on 1.0.X but untested)
* Haystack 1.X (http://github.com/toastdriven/django-haystack)


Setup
=====

#. Add ``saved_searches`` to ``INSTALLED_APPS``.
#. ``./manage.py syncdb``.
#. Alter either your URLconfs to use the ``saved_searches.views.SavedSearchView``
   or change the inheritance of your subclassed views.
