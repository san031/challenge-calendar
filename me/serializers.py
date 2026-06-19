from rest_framework import serializers
from .models import *

class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ['user','date','created_at','content','mood', 'mood_auto_detected']

class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = ['user','date','quote','quotedby']

        


    