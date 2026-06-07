from django.shortcuts import render
from .models import *
from .serializers import todoSerializer,todoItemSerializer,streakRecordSerializer
from rest_framework import viewsets,permissions,views
from rest_framework.response import Response
from account.authentication import JWTCookieAuthentication
from account.serializers import UserSerializer
from rest_framework import status
from rest_framework.authentication import BasicAuthentication

# Create your views here.

class validateUserView(views.APIView):
    permission_classes = [permissions.AllowAny]
    # authentication_classes = [JWTCookieAuthentication]

 
    def get(self,request):
        serializer = UserSerializer(request.user)
        return Response({
            "isAuthenticated":True,
            "email":request.user.email
        })

class todoviewsets(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = todoSerializer
    queryset = Todo.objects.all()

    def post(self, request, *args, **kwargs):
        today,created = Todo.objects.get_or_create(
            user = request.user,
            created_at = date.today()
        )

        if not created:
            serializer = self.serializer_class(today)
            return Response(serializer.data, status =  status.HTTP_200_OK)
        serializer = self.serializer_class(today)
        # serializer.is_valid(raise_exception = True)
        # serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    

    def get(self,request):
        q = Todo.objects.filter(user = request.user)
        print(f"gettodolist: {q}")
        serializer = self.serializer_class(q, many = True)
        print(f"gettodoserializer:{serializer} {serializer.data }")
        return Response(serializer.data)
    
class todolistviewsets(viewsets.ViewSet):
    serializer_class = todoItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTCookieAuthentication]
    def update(self,request,id = None):
        to_check_todo = ItemTodo.objects.get (id = id)
        serializer = self.serializer_class(to_check_todo,data = request.data,partial =True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data) 

    def post(self,request,*args, **kwargs):

        todo, created = Todo.objects.get_or_create(
            user = request.user,
            created_at = date.today()  
        )
        serializer = self.serializer_class(data = request.data)

        serializer.is_valid(raise_exception = True)
        serializer.save(items = todo) # here arguement within serializer.save() helps to relate the object created within Todo with foreign key of TodoItem    
        return Response(serializer.data)
    
    def removetodo(self,request,id = None):
        todo_item = ItemTodo.objects.get(id = id)
        todo_item.delete()
        return Response("deletion successful")


class streakRecordviewsets(viewsets.ViewSet):
    serializer_class = streakRecordSerializer()
    def getpercentagetaskcompleted(self,request):
        # usr = streakRecord.objects.filter(user = request.user )
        todos = streakRecord.objects.filter(user = request.user).prefetch_related('todo')
        serializer = streakRecordSerializer(todos, many = True)
        return Response(serializer.data)

        # todos = Todo.objects.filter(user = request.user).prefetch_related('todo_item')

        # result = []
        # for todo in todos:
        #     result.append({
        #         "dateid":str(todo.created_at)
        #         "todo":todoSerializer(todo).data,
        #         "completion_percentage":calcul
        #     })


class streakHistoryView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = streakRecordSerializer
    def get(self,request):
        user = request.user
        current_year = date.today().year

        start_date = date(current_year, 1,1)
        end_date = date(current_year,12,31)

        records = streakRecord.objects.filter(
            user = user,
            dateid__range= [start_date,end_date]
        ).select_related('todo').prefetch_related('todo__todo_item')

        # .values() won't work since it only fetches actual DB columns.
        # result = [
        #     {
        #         "dateid": str(entry['dateid']),
        #         "completion_percentage": entry['completion_percentage']
        #     }
        #     for entry in completions
        # ]

        serializer = self.serializer_class(records, many = True)

        return Response(serializer.data)


