from django.contrib import admin
from .models import Todo,ItemTodo,streakRecord
# Register your models here.
admin.site.register(Todo)
admin.site.register(ItemTodo)
admin.site.register(streakRecord)