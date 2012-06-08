from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('example.core.views',
    url(r'^formset/', 'formset', name='example-formset'),    
    url(r'^advanced/', 'advanced', name='example-advanced'),
    url(r'^', 'index', name='example-index'),
)
