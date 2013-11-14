from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'OEMS.views.home', name='home'),
    # url(r'^OEMS/', include('OEMS.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),


    #Student related
    url(r'^student/$', 'student.views.index', name='student_index'),
    url(r'^student/dashboard/$', 'student.views.dashboard',
        name='student_dashboard'),
    url(r'^student/profile/$', 'student.views.profile',
        name='student_profile'),
    url(r'^student/profile/update/$', 'student.views.update_profile',
        name='update_student_profile'),
    url(r'^student/signin/$', 'student.views.sign_in',
        name='student_signin'),
    url(r'^student/signout/$', 'student.views.sign_out',
        name='student_signout'),

    #Student Experimnt Related
    url(r'^student/experiment/(?P<experiment_id>\d+)/$',
        'student.views.experiment_information',
        name='experiment_info_for_student'),
    url(r'^student/experiment_list/$',
        'student.views.experiment_list_for_picked_lesson',
        name='student_list_experiment'),


    #Student Lesson Related
    url(r'^student/lesson_list/$', 'student.views.has_pick_lesson_list',
        name='student_list_lesson'),
    url(r'^student/lesson/(?P<lesson_id>\d+)/$',
        'student.views.lesson_information',
        name='lesson_info_for_student'),
    url(r'^student/lesson/search/$', 'student.views.search_lesson',
        name='search_lesson_by_student'),
    url(r'^student/lesson/subscribe/$',
        'student.views.subscribe_lesson',
        name='student_subscribe'),
    url(r'^student/lesson/(?P<lesson_id>\d+)/subscribe/$',
        'student.views.subscribe_lesson_handle',
        name='student_subscribe_handle'),
    url(r'^student/lesson/unsubscribe/$',
        'student.views.unsubscribe_lesson',
        name='student_unsubscribe'),
    url(r'^student/lesson/(?P<lesson_id>\d+)/unsubscribe/$',
        'student.views.unsubscribe_lesson_handle',
        name='student_unsubscribe_handle'),


    #Student Experiment Related
    url(r'^student/submit_report/(?P<experiment_id>\d+)$',
        'student.views.submit_report',
        name="submit_report"),
    url(r'^student/experiment/(?P<experiment_id>\d+)/$',
        'student.views.experiment_information',
        name="student_experiment_info"),

    #Student Experiment Report Related
    url(r'^tecaher/experiment_report/(?P<experiment_report_id>\d+)/evaluate/$',
        'teacher.views.experiment_report_evaluate',
        name='experiment_report_evaluate'),


    #Teacher Related
    url(r'^teacher/$', 'teacher.views.index', name='teacher_index'),
    url(r'^teacher/dashboard/$', 'teacher.views.dashboard',
        name='teacher_dashboard'),
    url(r'^teacher/signin/$', 'teacher.views.sign_in',
        name='teacher_signin'),
    url(r'^teacher/signout/$', 'teacher.views.sign_out',
        name='teacher_signout'),
    url(r'^teacher/profile/$', 'teacher.views.teacher_profile',
        name='teacher_profile'),

    #Teacher Lesson Category Related
    url(r'^teacher/category/create/$',
        'experiment.views.create_lesson_category',
        name='create_lesson_category'),
    url(r'^teacher/category/list/$',
        'experiment.views.lesson_category_list', name="category_list"),

    #Teacher Lesson Related
    url(r'^teacher/lesson/create/$', 'experiment.views.create_lesson',
        name='create_lesson'),
    url(r'^teacher/lesson/(?P<lesson_id>\d+)/$',
        'experiment.views.lesson_information', name="lesson_info"),
    url(r'^teacher/lesson/(?P<lesson_id>\d+)/update$',
        'experiment.views.update_lesson', name='update_lesson'),
    url(r'^teacher/lesson/(?P<lesson_id>\d+)/delete/$',
        'experiment.views.delete_lesson', name='delete_lesson'),
    url(r'^teacher/lesson_list/$', 'experiment.views.lesson_list_all',
        name="teacher_lesson_list_all"),
    url(r'^teacher/lesson_list/(?P<category_id>\d+)/$',
        'experiment.views.lesson_list', name="teacher_lesson_list"),

    #Teacher Experiment Related
    url(r'^teacher/create_experiment/(?P<lesson_id>\d+)/$',
        'experiment.views.create_experiment', name="create_experiment"),
    url(r'^teacher/experiment/(?P<experiment_id>\d+)/$',
        'experiment.views.experiment_information', name="experiment_info"),
    url(r'^teacher/experiment/(?P<experiment_id>\d+)/delete/$',
        'experiment.views.delete_experiment', name='delete_experiment'),


    #Teacher Experiment Report Related
    url(r'^teacher/experiment/(?P<experiment_id>\d+)/modify/$',
        'experiment.views.experiment_modify', name='experiment_modify'),





)
