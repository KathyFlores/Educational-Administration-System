from django.conf.urls import url, include
from .scheduling import room, course,arrange
from . import views

urlpatterns = [
    url(r'^api/scheduling/room/$', room.api_room),
    url(r'^api/scheduling/room/getpagecount/$', room.api_room_get_pagecount),
    url(r'^api/scheduling/room/delete/$', room.api_room_delete),
    url(r'^api/scheduling/course/$', course.api_course),
    url(r'^api/scheduling/course/delete/$', course.api_course_delete),
    url(r'^api/scheduling/course/update/$', course.api_course_update),
    url(r'^api/scheduling/course/getpagecount/$', course.api_course_get_pagecount),
    url(r'^api/scheduling/arrange*',arrange.api_arrange),

    url(r'^arrangement/$', views.arrangement, name="arrangement"),
    url(r'^calender/$', views.calender, name="calender"),
    url(r'^classroom/$', views.classroom, name='classroom')
]