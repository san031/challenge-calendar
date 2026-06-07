from django.urls import path,include
from .views import *

urlpatterns = [
    path('newtodo/',todoviewsets.as_view({'post':'post'})),
    path('gettodo/',todoviewsets.as_view({'get':'get'})),
    path('newtodoitem/',todolistviewsets.as_view({'post':'post'})),
    path('updatetodoitem/<int:id>/',todolistviewsets.as_view({'patch':'update'})),
    path('removetodoitem/<int:id>/',todolistviewsets.as_view({'delete':'removetodo'})),
    path('streak/getpercentage/', streakRecordviewsets.as_view({'get': 'getpercentagetaskcompleted'})),
    path('streak/history/', streakHistoryView.as_view({'get':'get'})),
    path('me/',validateUserView.as_view())
]
