from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
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

    url(r'^teacher/experiment/created_success/$', 'experiment.views.created_success', name='created_success'),
    url(r'^teacher/display-experiment/$','experiment.views.display_experiment', name="display_experiment_list"),
    url(r'^teacher/create_lesson_category/$', 'experiment.views.create_lesson_category', name='create_lesson_category'),
    url(r'^teacher/create_experiment/$', 'experiment.views.create_experiment', name="create_experiment"),
    url(r'^teacher/create_lesson/$', 'experiment.views.create_lesson', name='create_lesson'),
)
