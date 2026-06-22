from django.db import models
from account.models import User
from cloudinary.models import CloudinaryField


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
    date = models.DateField(auto_now=True)
    quote = models.TextField()
    quotedby =  models.CharField(max_length=50,blank=True, null= True)
    created_at = models.DateTimeField(auto_now_add=True)

class Catalog(models.Model):

    CATEGORY_CHOICES = [
        ('hobbies',"Hobbies"),
        ('travel','Travel'),
        ('shopping','Shopping'),
        ('food','Food'),
        ('people',"People"),
        ('sports',"Sports"),
        ('miscellaneous','Miscellaneous')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    is_done = models.BooleanField(default=False)
    category = models.CharField(max_length=50,choices = CATEGORY_CHOICES, blank=True, null= True)
    address = models.TextField()
    date_added = models.DateField(auto_now=True)
    thumbnail = CloudinaryField(
        'image',
        folder='thumbnail_catalog/',   # organizes inside cloudinary dashboard
        null=True,
        blank=True
    )
    #add category
    

        

