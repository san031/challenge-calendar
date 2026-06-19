from django.shortcuts import render
from .models import JournalEntry
from .serializers import JournalEntrySerializer
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