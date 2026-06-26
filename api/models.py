from django.db import models
from datetime import date
from account.models import User
from django.core.cache import cache
# Create your models here.

def default_title():
    return date.today().strftime("%d%m%y")
    #strftime converts the date/datetime object into a formatted string based on format codes provided
class Todo(models.Model):

    head = models.CharField(max_length=50,default=default_title)
    created_at = models.DateField( auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together  = ['user','created_at']    

    def __str__(self):
        return self.head

class ItemTodo(models.Model):
    title = models.CharField(max_length=50)
    is_done = models.BooleanField(default=False)
    items = models.ForeignKey(Todo, on_delete=models.CASCADE,null=True,related_name='todo_item')

    def __str__(self):
        return self.title


class streakRecord(models.Model):
    dateid = models.DateField(default  = date.today)
    todo = models.OneToOneField(Todo, on_delete=models.CASCADE, )
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        unique_together = ['dateid','todo','user']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Wipe the cache for this specific user upon new activity
        cache.delete(f"user_monthly_streak_{self.user.id}")

    




