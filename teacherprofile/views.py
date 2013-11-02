from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import Http404

from teacherprofile.models import TeacherProfile
from teacher.utils import is_teacher
from teacherprofile.forms import TeacherProfileForm


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def teacher_profile(request):
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("edit_success")
    else:
        form = TeacherProfileForm(instance=request.user.profile)
    args = {}
    args['form'] = form
    return render(request, 'teacher/profile.html', args)


@login_required(login_url='teacher')
@is_teacher(redirect_url='')
def edit_success(request):
    return render(request, 'teacher/edit_success.html', {})
