from django.db import models
from account.models import User

# Create your models here.
class JournalEntry(models.Model):

    MOOD_CHOICES = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('anxious', 'Anxious'),
        ('angry', 'Angry'),
        ('calm', 'Calm'),
        ('excited', 'Excited'),
        ('grateful', 'Grateful'),
        ('frustrated', 'Frustrated'),
        ('neutral', 'Neutral'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    mood = models.CharField(max_length=50,choices = MOOD_CHOICES, blank=True, null= True)
    mood_auto_detected = models.BooleanField(default=False)



    class Meta:
        unique_together = ('user','date')
        ordering = ['-date']

class Quotation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    quote = models.TextField()
    quotedby =  models.CharField(max_length=50,blank=True, null= True)
    created_at = models.DateTimeField(auto_now_add=True)

    

        

