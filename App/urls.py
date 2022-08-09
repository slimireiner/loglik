from django.urls import path

from . import views
from .views import TokenCreate, RegisterView, ChildAdd, AddTask, ScoreList
import App.views
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenCreate.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('add_child/', ChildAdd.as_view(), name='add_child'),
    path('add_task/', AddTask.as_view(), name='add_task'),
    path('update_task/', App.views.update_task, name='update_task'),
    path('get_scores/<int:score_id>/', App.views.get_scores, name='get_score'),
    path('get_all_scores/', ScoreList.as_view(), name='get_all_score'),
]
