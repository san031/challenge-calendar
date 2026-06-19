from django.urls import path,include
from .views import *

urlpatterns = [
    path('journalentry/',JournalEntryViewset.as_view({'post':'post'}))
]