from django.conf.urls import url

from . import views

app_name = 'online_test'
urlpatterns = [
    url('subjects/student', views.SubjectsStudentView.as_view(), name='subjects_student'),
    url('subjects/teacher', views.SubjectsTeacherView.as_view(), name='subjects_teacher'),
    url('subject/(?P<subject>[0-9a-zA-Z]+)/tests', views.TestsView.as_view(), name='tests'),
    url('test/(?P<pk>[0-9]+)/', views.TestDetail.as_view(), name='test_detail'),
    url('test/submit_answer/', views.submit_answer, name='judge'),
    url('subject/(?P<subject>[0-9a-zA-Z]+)/statistics/teacher/tests', views.TeacherStatisticsTests.as_view(),
        name='teacher_statistics_tests'),
    url('subject/(?P<subject>[0-9a-zA-Z]+)/statistics/teacher/chapters', views.TeacherStatisticsChapters.as_view(),
        name='teacher_statistics_chapters'),
    url('subject/(?P<subject>[0-9a-zA-Z]+)/statistics/teacher/knowledge_points',
        views.TeacherStatisticsKnowledgePoints.as_view(), name='teacher_statistics_knowledge_points'),
    url('subject/(?P<subject>[0-9a-zA-Z]+)/statistics/student/', views.StudentStatistics.as_view(),
        name='student_statistics'),
    url('test_statistics/(?P<pk>[0-9]+)/', views.TestStatistics.as_view(), name='test_statistics'),
    url('test_statistics/student/(?P<pk>[0-9]+)/(?P<student_pk>[0-9a-zA-Z]+)/',
        views.TestStatisticsStudentRecord.as_view(), name='test_statistics_student_record'),
    url('test_statistics/teacher/(?P<pk>[0-9]+)/(?P<student_pk>[0-9a-zA-Z]+)/',
        views.TestStatisticsTeacherRecord.as_view(), name='test_statistics_teacher_record'),

    url('problem_bank/single_problem/choice/(?P<pk>[0-9a-zA-Z]+)/', views.SingleChoice.as_view(), name='problem_choice'),
    url('problem_bank/single_problem/judge/(?P<pk>[0-9a-zA-Z]+)/', views.SingleJudge.as_view(), name='problem_judge'),
    url('problem_bank/single_problem/static/choice/(?P<pk>[0-9a-zA-Z]+)/', views.SingleStaticChoice.as_view(),
        name='static_choice'),
    url('problem_bank/single_problem/static/judge/(?P<pk>[0-9a-zA-Z]+)/', views.SingleStaticJudge.as_view(),
        name='static_judge'),
    url('problem_bank/single_problem', views.SingleProblem.as_view(), name='problem_single'),
    url('problem_bank/search/', views.problem_search, name="problem_search"),
    url('problem_bank/add/', views.problem_add, name="problem_add"),
    url('problem_bank/(?P<pk>[0-9a-zA-Z]+)/mod/', views.problem_mod, name="problem_mod"),
    url('problem_bank/(?P<pk>[0-9a-zA-Z]+)/del/', views.problem_del, name="problem_del"),
    url('problem_bank/detail/', views.ProblemDetail.as_view(), name="problem_detail"),
    url('problem_bank/', views.ProblemBank.as_view(), name='problem_bank'),

    url('teacher/test/auto-generation/(?P<pk>[0-9a-zA-Z]+)/del/', views.test_del, name="test_del"),
    url('teacher/test/auto-generation/(?P<pk>[0-9a-zA-Z]+)/mod/', views.test_mod, name="test_mod"),
    url('teacher/test/auto-generation/add/', views.test_add, name="test_add"),
    url('teacher/test/auto-generation/gerner/', views.test_gerner, name="test_gerner"),
    url('teacher/test/auto-generation/search/', views.test_search, name="test_search"),
    url('teacher/test/auto-generation', views.AutoTestGeneration.as_view(), name='auto_test_generation'),

]
