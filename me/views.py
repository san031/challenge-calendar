from django.shortcuts import render
from .models import JournalEntry, Quotation,Catalog
from .serializers import JournalEntrySerializer, QuotationSerializer, CatalogSerializer
from rest_framework.response import Response
from account.authentication import JWTCookieAuthentication
from account.serializers import UserSerializer
from rest_framework import status,viewsets,permissions,views
from .utils import detect_mood
# Create your views here.


class JournalEntryViewset(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JournalEntrySerializer
    

    def post(self,request):
        # journal = JournalEntry.objects.get(id = journal_id, user = request.user)
        date = request.data.get('date')
        content = request.data.get('content')
        mood = request.data.get('mood')

        if not mood and content:
            mood = detect_mood(content)

        entry,created = JournalEntry.objects.update_or_create(
            user = request.user,
            date = date,
            defaults={
                'content': content,
                'mood': mood,
            }
        )

        serializer = self.serializer_class(entry)

        return Response(serializer.data, status = status.HTTP_201_CREATED)
    
    def get(self,request):
        q = JournalEntry.objects.filter(user = request.user)
        serializer = self.serializer_class(q, many = True)
        return Response(serializer.data)
    
class QuotationViewset(viewsets.ViewSet):

    serializer_class = QuotationSerializer
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [JWTCookieAuthentication]

    def post(self,request):
        # quotation = Quotation.objects.update_or_create(
        #     user = request.user,
        # )

        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save(user = request.user) # here arguement within serializer.save() helps to relate the object created within foreign key     
        return Response(serializer.data)
    
    
    def get(self,request):
        q = Quotation.objects.filter(user = request.user)
        serializer = self.serializer_class(q, many = True)
        return Response(serializer.data)
    

class CatalogViewset(viewsets.ViewSet):
    serializer_class = CatalogSerializer
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [JWTCookieAuthentication]


    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save(user = request.user) # here arguement within serializer.save() helps to relate the object created within foreign key     
        return Response(serializer.data)
    
    def get(self,request):
        q = Catalog.objects.filter(user = request.user)
        serializer = self.serializer_class(q, many = True)
        return Response(serializer.data)
        
