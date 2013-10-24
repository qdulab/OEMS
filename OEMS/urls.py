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
    url(r'^index/$', 'experiment.views.index', name="index"), 
    url(r'^display-experiment/$','experiment.views.display_experiment', name="display_experiment_list"),
    url(r'^create_lesson_category/$', 'experiment.views.create_lesson_category', name='create_lesson_category'),
    url(r'^create_experiment/$', 'experiment.views.create_experiment', name="create_experiment"),
    url(r'^create_lesson/$', 'experiment.views.create_lesson', name='create_lesson'),
)
