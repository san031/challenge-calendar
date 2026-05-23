from rest_framework import serializers
from .models import *

class todoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemTodo
        fields = ['id','title','is_done','items']

class todoSerializer(serializers.ModelSerializer):
    todolist = serializers.SlugRelatedField(
        many = True,
        read_only = True,
        slug_field = 'title'
    )
    todo_item = todoItemSerializer(read_only = True,many =True, )
    class Meta:
        model = Todo
        fields = ['id','user','head','created_at','todolist','todo_item']

    # def create(self,validated_data):
    #     item_data = validated_data.pop('todo_item')
    #     print(f"itemData: {item_data}")
    #     todo =  Todo.objects.create(**validated_data)
    #     for item in item_data:
    #         ItemTodo.objects.create(todo = todo, **item)
    #     return todo