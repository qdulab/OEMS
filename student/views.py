from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render


@login_required(login_url='student_index')
def dashboard(request):
    return render(request, 'student/dashboard.html', {})

def index(request):
    if hasattr(request, 'user') and isinstance(request.user, User):
        return redirect('student_dashboard')
    return render(request, 'student/index.html', {})

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        student = authenticate(username=username, password=password)
        if student is not None and isinstance(student, User):
            login(request, student)
            return redirect('student_dashboard')
    return redirect('student_dashboard')
        
@login_required(login_url='student_index')
def sign_out(request):
    logout(request)
    return redirect('student_index')
