from django.conf.urls import url

from onlineTest import views

app_name = 'onlineTest'
urlpatterns = [
		url('problem_bank/search/', views.problem_search, name="problem_search"),
    url('problem_bank/add/', views.problem_add, name="problem_add"),
    url('problem_bank/(?P<pk>[0-9]+)/mod/', views.problem_mod, name="problem_mod"),
    url('problem_bank/(?P<pk>[0-9]+)/del/', views.problem_del, name="problem_del"),
    url('problem_bank/detail/', views.problem_del, name="problem_detail"),
    url('problem_bank/', views.ProblemBank.as_view(), name='problem_bank'),

    url('teacher/test/auto-generation/(?P<pk>[0-9]+)/del/', views.test_del, name="test_del"),
    url('teacher/test/auto-generation/(?P<pk>[0-9]+)/mod/', views.test_mod, name="test_mod"),
    url('teacher/test/auto-generation/add/', views.test_add, name="test_add"),
    url('teacher/test/auto-generation/search/', views.test_search, name="test_search"),
    url('teacher/test/auto-generation', views.AutoTestGeneration.as_view(), name='auto_test_generation'),


    url('', views.IndexView.as_view(), name='index'),
    url('test/(?P<pk>[0-9]+)/', views.TestDetail.as_view(), name='test_detail'),
    url('test/submit_answer/', views.submit_answer, name='judge'),
    url('statistics/teacher/tests', views.TeacherStatisticsTests.as_view(), name='teacher_statistics_tests'),
    url('statistics/teacher/chapters', views.TeacherStatisticsChapters.as_view(), name='teacher_statistics_chapters'),
    url('statistics/teacher/knowledge_points', views.TeacherStatisticsKnowledgePoints.as_view(),
         name='teacher_statistics_knowledge_points'),
    url('statistics/student/', views.StudentStatistics.as_view(), name='student_statistics'),
    url('test_statistics/<int:pk>/', views.TestStatistics.as_view(), name='test_statistics'),
    url('test_statistics/<int:pk>/<int:student_pk>/', views.TestStatisticsStudentRecord.as_view(),
         name='test_statistics_student_record'),
    url('test_statistics/teacher/(?P<pk>[0-9]+)/(?P<student_pk>[0-9]+)/', views.TestStatisticsTeacherRecord.as_view(),
         name='test_statistics_teacher_record'),
    # url('chapter_statistics/<int:pk>', views.TeacherStatisticsChapters.as_view(), name='teacher_statistics_chapters')
]
