from django.shortcuts import render
from .models import *
from .serializers import todoSerializer,todoItemSerializer
from rest_framework import viewsets,permissions
from rest_framework.response import Response

# Create your views here.

class todoviewsets(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = todoSerializer
    queryset = Todo.objects.all()

    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(data = request.data )
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)
    
    def get(self,request):
        q = Todo.objects.filter(user = request.user)
        print(q)
        serializer = self.serializer_class(q, many = True)
        return Response(serializer.data)
    
class todolistviewsets(viewsets.ViewSet):
    serializer_class = todoItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self,request,id = None):
        to_check_todo = ItemTodo.objects.get (id = id)
        serializer = self.serializer_class(to_check_todo,data = request.data,partial =True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def post(self,request,*args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)
    
    def removetodo(self,request,id = None):
        todo_item = ItemTodo.objects.get(id = id)
        todo_item.delete()
        return Response("deletion successful")


