from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from .models import Task, User
from .forms import TaskForm 


def registerPage(request):
    page='register'
    form=UserCreationForm()
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            new_user=form.save()
            login(request,new_user)
            return redirect('task-list')
    context={'page':page, 'form': form}
    return render(request, 'tasks/login_register.html', context)

def loginPage(request):
    page='login'
        
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('task-list')
        else:
            return HttpResponse('Login Failed :( ')
    context = {'page':page}
    return render(request, 'tasks/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def userTasks(request, pk):
    user = User.objects.get(id=pk)
    tasks = Task.objects.filter(user=user)
    context = {'user': user, 'tasks': tasks}
    return render(request, 'tasks/user_tasks.html', context)

class Task_List(View):
    template_name= 'tasks/task_list.html'
    
    def get(self, request):
        tasks = Task.objects.all().order_by('-updated_at')
        users =User.objects.all()
        
        if not request.user.is_authenticated:
           return redirect('login')
       
        context ={'tasks': tasks, 'users': users}
        return render(request, self.template_name, context)
    
    
    
class Task_Details(View):
    template_name= 'tasks/task_details.html'
    
    def get(self, request, pk):
        task = get_object_or_404(Task, id=pk)
        
        context  = {'task': task}
        return render(request, self.template_name, context)    
    
    
class Task_Create(View):
    template_name= 'tasks/create_task.html'
    def get(self, request):
        form = TaskForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task-list')
        context = {'form': form}
        return render(request, self.template_name, context)
    
    

class Update_Delete(View):
    
    template_name = 'tasks/edit_task.html'
    
    def get(self,request, pk):
        task = get_object_or_404(Task, id=pk)
        form = TaskForm(instance=task)
      
        if request.user != task.user:
          return HttpResponse("This task was created by another user. You have no business here!!")
      
        context = {'form':form}
        return render(request, self.template_name, context )
    
    
    def post(self,request, pk):
        task = get_object_or_404(Task, id=pk)
        form = TaskForm(request.POST, instance=task)
        
        
        if 'edit' in request.POST and form.is_valid():
            form.save()
            return redirect('task-list')
        
        if 'delete' in request.POST:
            task.delete()
            return redirect('task-list')            
        
        context = {'task': task, 'form': form}
        return render(request, self.template_name, context )