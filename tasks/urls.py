from django.urls import path
from . import views

urlpatterns = [
    path('',views.Task_List.as_view(), name='task-list'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('user-tasks/<str:pk>/', views.userTasks, name= "user-tasks"),
    path('task-details/<str:pk>', views.Task_Details.as_view(), name='task-details'),
    path('create-task/', views.Task_Create.as_view(), name='create-task'),
    path('edit-task/<str:pk>', views.Update_Delete.as_view(), name='edit-task'),
    path('delete-task/<str:pk>', views.Update_Delete.as_view(), name='delete-task'),
]
