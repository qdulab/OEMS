from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect, render
from teacher.models import Teacher

def user_login(request):
  #  import pdb; pdb.set_trace()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    	user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if isinstance (user,Teacher):
                return rende(request,'../templates/base.html', {'username':username}) #TODO URL->teacher.html
            else:
                return rende(request,'../templates/base.html', {'username':username}) #TODO URL->student.html
        else:
            return render(request,'../templates/base.html') #when the user not in SQL
    else:
        return render(request,'../templates/base.html') #when request.method is not POST

@login_required()   #TODO  add:(login_url='/teacher/login'  or /strudent/login)
def user_logout(request):
    logout(request)
    return render(request,'../templates/base.html')
