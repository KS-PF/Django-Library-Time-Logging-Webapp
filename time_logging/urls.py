from django.urls import path
from . import views
from .views  import (
    Enter, Add, Exit, ExitExecute,
)
from django.contrib.auth.decorators import login_required

app_name = 'time_logging'
urlpatterns = [
    path('', views.index, name='index'),
    path('enter/', Enter.as_view(), name='enter'),
    path('exit/', Exit.as_view(), name='exit'),
    path('exit/<int:pk>/', ExitExecute.as_view(), name='exit_execute'),
    path('add/', Add.as_view(), name='add'),
    path('use/', views.use, name='use'),
    path('message/<str:type>/', views.message, name='message'),
]
