from django.conf.urls import patterns, include, url
from experiment.views import display_experiment, create_experiment

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
    url(r'^display-experiment/$', display_experiment, name="display_experiment_list"),
    url(r'^create_lesson_category/$', 'experiment.views.create_lesson_category', name='create_lesson_category'),
    url(r'^create_experiment/$', create_experiment, name="create_experiment")
)
