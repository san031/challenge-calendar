from django.contrib import admin
from .models import JournalEntry,Quotation, Catalog
# Register your models here.


admin.site.register(JournalEntry)
admin.site.register(Quotation)
admin.site.register(Catalog)