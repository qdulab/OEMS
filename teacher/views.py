from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get['username']
        password = request.POST.get['password']
    	user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render_to_response('../templates/side_bar.html', {'username':username}) #needChange: URL
        else:
            return redirect('index') #when the user not in SQL
    else:
        return redirect('index') #when request.method is not POST

@login_required()   #needChange: (login_url='/teacher/login'  or /strudent/login)
def user_logout(request):
    logout(request)
    return redirect('index')
