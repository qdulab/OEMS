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

    url(r'^teacher/$', 'teacher.views.index', name='teacher_index'),
    url(r'^teacher/dashboard/$', 'teacher.views.dashboard', name='teacher_dashboard'),
    url(r'^teacher/signin/$', 'teacher.views.sign_in', name='teacher_signin'),
    url(r'^teacher/signout/$', 'teacher.views.sign_out', name='teacher_signout'),

    url(r'^teacher/experiment/created_success/$',
         'experiment.views.created_success', name='created_success'),
    url(r'^teacher/lesson/(?P<lesson_id>\d+)/$',
        'experiment.views.lesson_information', name="lesson_info"),
    url(r'^teacher/experiment/(?P<experiment_id>\d+)/$',
        'experiment.views.experiment_information', name="experiment_info"),
    url(r'^teacher/create_lesson_category/$',
        'experiment.views.create_lesson_category',
        name='create_lesson_category'),
    url(r'^teacher/create_experiment/(?P<lesson_id>\d+)/$',
        'experiment.views.create_experiment',
        name="create_experiment"),
    url(r'^teacher/create_lesson/$', 'experiment.views.create_lesson',
        name='create_lesson'),
    url(r'^teacher/lesson_list/(?P<category_id>\d+)/$','experiment.views.lesson_list',
        name="teacher_lesson_list"),
    url(r'^teacher/experiment/create_success/$',
        'experiment.views.create_experiment_success',
        name='create_experiment_success'),
    url(r'^teacher/experiment/delete/(?P<experiment_id>\d+)/$',
        'experiment.views.delete_experiment',
        name='delete_experiment'),
    url(r'^teacher/lesson/delete/(?P<lesson_id>\d+)/$', 
        'experiment.views.delete_lesson',
        name='delete_lesson'),
    url(r'^teacher/delete_success/$',
        'experiment.views.delete_success', 
        name='delete_success'),
    url(r'^teacher/lesson_category_list/$',
        'experiment.views.lesson_category_list', 
        name="category_list"),
    url(r'^teacher/experiment/modify/(?P<experiment_id>\d+)/$',
        'experiment.views.experiment_modify', 
        name='experiment_modify'),
)
