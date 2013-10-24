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
    url(r'^teacher/$', 'teacher.views.teacher_login', name='teacher_index'),
    url(r'^teacher/dashboard/$', 'teacher.views.teacher_login', name='teacher_dashboard'),
    url(r'^teacher/logout/$', 'teacher.views.teacher_logout', name='teacher_logout'),
    url(r'^teacher/display-experiment/$','experiment.views.display_experiment', name="display_experiment_list"),
    url(r'^teacher/create_lesson_category/$', 'experiment.views.create_lesson_category', name='create_lesson_category'),
    url(r'^teacher/create_experiment/$', 'experiment.views.create_experiment', name="create_experiment"),
    url(r'^teacher/create_lesson/$', 'experiment.views.create_lesson', name='create_lesson'),
)
