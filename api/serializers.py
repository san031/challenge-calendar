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


class streakRecordSerializer(serializers.ModelSerializer):
    todo = todoSerializer(read_only = True,)  
    completion_percentage = serializers.SerializerMethodField()   
    #A read-only field that get its representation from calling a method on the parent serializer class. 
    # The method called will be of the form "get_{field_name}", 
    # and should take a single argument, which is the object being serialized.
    class Meta:
        model = streakRecord
        fields = ['dateid','todo','completion_percentage']

    def get_completion_percentage(self,obj):
        todo = obj.todo

        total = todo.todo_item.count()

        if total == 0:
            return None
        
        completed = todo.todo_item.filter(is_done = True).count()

        return round((completed/total)*100,2)
