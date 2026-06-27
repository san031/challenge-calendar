from django.shortcuts import render
from .models import *
from .serializers import todoSerializer,todoItemSerializer,streakRecordSerializer
from rest_framework import viewsets,permissions,views
from rest_framework.response import Response
from account.authentication import JWTCookieAuthentication
from account.serializers import UserSerializer
from rest_framework import status
import calendar
# from rest_framework.authentication import BasicAuthentication

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
    serializer_class = streakRecordSerializer
    def getpercentagetaskcompleted(self,request):
        user = request.user
        
        # Get all todos for the user
        todos = Todo.objects.filter(user=user).prefetch_related('todo_item')
        
        if not todos.exists():
            return Response({
                'total_tasks': 0,
                'completed_tasks': 0,
                'completion_percentage': 0
            }, status=status.HTTP_200_OK)
        
        # Calculate total and completed tasks across all todos
        total_tasks = 0
        completed_tasks = 0
        
        for todo in todos:
            total_tasks += todo.todo_item.count()
            completed_tasks += todo.todo_item.filter(is_done=True).count()
        
        # Calculate overall completion percentage
        completion_percentage = round((completed_tasks / total_tasks) * 100, 2) if total_tasks > 0 else 0
        
        return Response({
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_percentage': completion_percentage
        }, status=status.HTTP_200_OK)

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

    def get(self, request):
        user = request.user
        current_year = date.today().year

        todos = Todo.objects.filter(
            user=user,
            created_at__year=current_year
        ).prefetch_related('todo_item')

        result = []
        for todo in todos:
            items = todo.todo_item.all()
            total = items.count()
            completed = items.filter(is_done=True).count()
            percentage = round((completed / total * 100), 2) if total > 0 else 0

            result.append({
                "dateid": todo.created_at,
                "todo_head": todo.head,
                "total_tasks": total,
                "completed_tasks": completed,
                "completion_percentage": percentage
            })

        return Response(result)
    
class MonthlyStreakAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated] # Ensures request.user is populated

    def get(self, request, *args, **kwargs):
        user = request.user
        cache_key = f"user_monthly_streak_{user.id}"
        
        # 1. Attempt to grab cached data from Redis
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        # 2. Determine bounds for the current month
        today = date.today()
        start_date = today.replace(day=1)
        _, num_days = calendar.monthrange(today.year, today.month)
        end_date = today.replace(day=num_days)

        # 3. Fetch records for the user within this month
        records = streakRecord.objects.filter(
            user=user,
            dateid__gte=start_date,
            dateid__lte=end_date
        ).select_related('todo') # Optimizes performance to prevent N+1 queries

        # 4. Run data through the serializer
        serializer = streakRecordSerializer(records, many=True)
        serialized_data = serializer.data  

        # 5. Save output to Redis cache for 15 minutes (900 seconds)
        cache.set(cache_key, serialized_data, 900)

        return Response(serialized_data)


