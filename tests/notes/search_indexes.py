from haystack import indexes
from haystack import site
from notes.models import Note


class NoteIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(document=True, model_attr='content')


site.register(Note, NoteIndex)
