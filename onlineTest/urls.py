from django.conf.urls import url

from . import views


urlpatterns = [
		url(r'^problem_bank/search/', views.problem_search, name="problem_search"),
    url(r'^problem_bank/add/', views.problem_add, name="problem_add"),
    url(r'^problem_bank/(?P<pk>[0-9]+)/mod/', views.problem_mod, name="problem_mod"),
    url(r'^problem_bank/(?P<pk>[0-9]+)/del/', views.problem_del, name="problem_del"),
    url(r'^problem_bank/detail/', views.problem_del, name="problem_detail"),
    url(r'^problem_bank/', views.ProblemBank.as_view(), name='problem_bank'),

    url(r'^teacher/test/auto-generation/(?P<pk>[0-9]+)/del/', views.test_del, name="test_del"),
    url(r'^teacher/test/auto-generation/(?P<pk>[0-9]+)/mod/', views.test_mod, name="test_mod"),
    url(r'^teacher/test/auto-generation/add/', views.test_add, name="test_add"),
    url(r'^teacher/test/auto-generation/search/', views.test_search, name="test_search"),
    url(r'^teacher/test/auto-generation', views.AutoTestGeneration.as_view(), name='auto_test_generation'),


    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^test/(?P<pk>[0-9]+)/', views.TestDetail.as_view(), name='test_detail'),
    url(r'^test/submit_answer/', views.submit_answer, name='judge'),
    url(r'^statistics/teacher/tests', views.TeacherStatisticsTests.as_view(), name='teacher_statistics_tests'),
    url(r'^statistics/teacher/chapters', views.TeacherStatisticsChapters.as_view(), name='teacher_statistics_chapters'),
    url(r'^statistics/teacher/knowledge_points', views.TeacherStatisticsKnowledgePoints.as_view(),
         name='teacher_statistics_knowledge_points'),
    url(r'^statistics/student/', views.StudentStatistics.as_view(), name='student_statistics'),
    url(r'^test_statistics/<int:pk>/', views.TestStatistics.as_view(), name='test_statistics'),
    url(r'^test_statistics/<int:pk>/<int:student_pk>/', views.TestStatisticsStudentRecord.as_view(),
         name='test_statistics_student_record'),
    url(r'^test_statistics/teacher/(?P<pk>[0-9]+)/(?P<student_pk>[0-9]+)/', views.TestStatisticsTeacherRecord.as_view(),
         name='test_statistics_teacher_record'),
    # url('chapter_statistics/<int:pk>', views.TeacherStatisticsChapters.as_view(), name=r'^teacher_statistics_chapters')
]
