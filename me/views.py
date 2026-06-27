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

    def update(self,request,id=None):
        try:
            item = Quotation.objects.get(id = id)
        except Quotation.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(item, data = request.data, partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
    
    def nomoremotivation(self,request, id= None):
        del_quote = Quotation.objects.get(id = id)
        del_quote.delete()
        return Response("deletion successful")



    

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
        chosen_wishlist = request.query_params.get('category')
        q = Catalog.objects.filter(user = request.user)
        if chosen_wishlist:
            q = q.filter(category = chosen_wishlist)
        serializer = self.serializer_class(q, many = True)
        return Response(serializer.data)


    def update(self,request,id=None):
        item = Catalog.objects.get(id = id)
        serializer = self.serializer_class(item, data = request.data, partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_200_OK)
        
    def notanymore(self, request, id= None):
        del_wishlist = Catalog.objects.get(id = id)
        del_wishlist.delete()
        return Response("deletion Successful")