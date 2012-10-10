from django.conf.urls import patterns, include, url


urlpatterns = patterns('core.views',
    url(r'^formset/', 'formset', name='example-formset'),    
    url(r'^advanced/', 'advanced', name='example-advanced'),
    url(r'^', 'index', name='example-index'),
)
