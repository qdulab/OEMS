from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect, render

from teacher.models import Teacher

def teacher_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    	teacher = authenticate(username=username, password=password)
        if teacher is not None and teacher.is_active and isinstance(teacher,Teacher):
            login(request, teacher)
            return render(request,'teacher/dashboard.html', {'username':username})
    else:
        return render(request,'teacher/index.html')

#TODO  add:(login_url='/teacher/login')
@login_required()
def teacher_logout(request):
    logout(request)
    return redirect('teacher_index')
