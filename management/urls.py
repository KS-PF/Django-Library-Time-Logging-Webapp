from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from .views  import (
    Manage, Download, Analysis,
)

app_name = 'management'
urlpatterns = [
    path('', login_required(views.index), name='index'),
    path('list/', login_required(Manage.as_view()), name='list'),
    path('<int:log_id>/update/', login_required(views.ManageUpdate), name='update'),
    path('<int:log_id>/delete/', login_required(views.ManageDelete), name='delete'),
    path('download/', login_required(Download.as_view()), name='download'),
    path('analysis/', login_required(Analysis.as_view()), name='analysis'),
]
