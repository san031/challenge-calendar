from django.db import models
from datetime import date
from account.models import User

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





