==============
saved_searches
==============

Allows you to personalize search by storing a user's search history.

For use with Haystack (http://haystacksearch.org/).

**WARNING!!!**

This project has been updated to be compatible with Haystack 2.0.0-alpha!
If you need ``queued_search`` for Haystack 1.2.X, please use the 1.0.4 tag
or ``pip install queued_search==1.0.4``!


Requirements
============

* Django 1.2+
* Haystack 2.0.X (http://github.com/toastdriven/django-haystack)


Setup
=====

#. Add ``saved_searches`` to ``INSTALLED_APPS``.
#. ``./manage.py syncdb``.
#. Alter either your URLconfs to use the ``saved_searches.views.SavedSearchView``
   or change the inheritance of your subclassed views.
