from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth import views as auth_views
from django.contrib import admin
urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'test_app.views.index', name='index'),
    url(r'^login/', auth_views.login, {'template_name': 'test_app/login.html'}),
    url(r'^requests/$', 'test_app.views.requests', name='requests'),
    url(
        r'^api/requests/$',
        'test_app.views.last_requests',
        name='last_requests'
    ),
    url(r'^edit-user/$', 'test_app.views.edit_user', name='edit_user')
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
