from django.urls import path,include
from .views import *

urlpatterns = [
    path('journalentry/',JournalEntryViewset.as_view({'post':'post'})),
    path('getjournalentry/', JournalEntryViewset.as_view({'get':'get'})),
    path('quote/', QuotationViewset.as_view({'post':'post'})),
    path('staymotivated/',QuotationViewset.as_view({'get':'get'})),
    path('catalog/', CatalogViewset.as_view({'post':'post'})),
    path('wishlisted/', CatalogViewset.as_view({'get':'get'}))
]