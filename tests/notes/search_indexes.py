from haystack import indexes
from notes.models import Note


class NoteIndex(indexes.RealTimeSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='content')
    
    def get_model(self):
        return Note
