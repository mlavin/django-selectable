from django.conf.urls import handler404, handler500, patterns, include


handler404 = 'selectable.tests.views.test_404'
handler500 = 'selectable.tests.views.test_500'

urlpatterns = patterns('',
    (r'^selectable-tests/', include('selectable.urls')),
)
