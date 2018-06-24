from django.conf.urls import url, include
from . import views


urlpatterns = [
    # url(r'^$', views.?, name='?'),
    url(r'^courses/$',views.courses,name="courses"),
    url(r'^select', views.select, name="select"),
    url(r'^table', views.table, name="table"),
    url(r'^teacher', views.teacher, name="teacher"),
    url(r'^curriculum/',views.curriculum, name="curriculum"),
    url(r'^course_select/$',views.course_select,name="course_select"),
    url(r'^export',views.export_excel,name="export"),
    url(r'^control_panel/', views.control, name="control"),
    url(r'^import_student/', views.import_student, name="import"),
    url(r'^api/disciplines_options/get', views.get_discipline_options, name="get_discipline_options"),
    url(r'^api/disciplines_details/post',views.post_discipline_details, name="post_discipline_details"),
    url(r'^api/disciplines_details/get',views.get_discipline_details, name="get_discipline_details"),
    url(r'^api/courses/get', views.get_all_courses, name="get_all_course"),
    url(r'^api/required_courses/get', views.get_required_courses, name="get_required_courses"),
    url(r'^api/required_course/delete', views.remove_required_course, name="remove_required_course"),
]
