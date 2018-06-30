from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'jwsystem.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^course_select/', include('courseSelect.urls')),
    url(r"^basic/",include('basicInfo.urls')),
    url(r"^api/",include('basicInfo.apiUrls')),
    url(r'^forum/', include('forum.urls')),
    url(r'^course_arrange/', include('courseArrange.urls')),
    url(r'^online_test/', include('onlineTest.urls', namespace='online_test'))
]
