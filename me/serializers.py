from rest_framework import serializers
from .models import *

class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ['id','user','date','created_at','content','mood', 'mood_auto_detected']

class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = ['id','date','quote','quotedby']

        read_only_fields = ['user']

class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = ["id","user","title","is_done","address", "date_added", "thumbnail","category"]

        read_only_fields = ['user']


    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url   # ← returns full cloudinary URL
        return None

        


    