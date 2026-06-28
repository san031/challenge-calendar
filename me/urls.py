from django.urls import path,include
from .views import *

urlpatterns = [
    path('journalentry/',JournalEntryViewset.as_view({'post':'post'})),
    path('getjournalentry/', JournalEntryViewset.as_view({'get':'get'})),
    path('quote/', QuotationViewset.as_view({'post':'post'})),
    path('staymotivated/',QuotationViewset.as_view({'get':'get'})),
    path('editurmotivation/<int:id>/',QuotationViewset.as_view({'patch':'update'})),
    path('catalog/', CatalogViewset.as_view({'post':'post'})),
    path('wishlistdone/<int:id>/', CatalogViewset.as_view({'patch':'update'})),
    path('wishlisted/', CatalogViewset.as_view({'get':'get'})),
    path('undowishlisting/<int:id>/', CatalogViewset.as_view({'delete':'notanymore'})),
    path('motivationgonewrong/<int:id>/',QuotationViewset.as_view({'delete':'nomoremotivation'}))
    
]

#  path('motivationgonewrong/',QuotationViewset.as_view({'del'}))