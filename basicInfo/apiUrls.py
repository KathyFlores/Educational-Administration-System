from django.conf.urls import include, url
from django.contrib import admin

import basicInfo.api.account as api_account
import basicInfo.api.student as api_student
import basicInfo.api.teacher as api_teacher
import basicInfo.api.admin as api_admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'teachSystem.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r"^account/login$",api_account.api_account_post),
    url(r"^account/register$",api_account.api_account_register_post),
    url(r"^account/repassword$",api_account.api_account_repassword_post),
    url(r"^account/person$",api_account.api_account_person),
    url(r"^account/img$",api_account.api_account_img),

    url(r"^student/info$",api_student.api_student_info),
    url(r"^student/exam$",api_student.api_student_exam),
    url(r"^student/grade$",api_student.api_student_grade),
    url(r"^teacher/info$",api_teacher.api_teacher_info),
    url(r"^teacher/course$",api_teacher.api_teacher_course),
    url(r"^teacher/addcourse$",api_teacher.api_teacher_addcourse),
    url(r"^teacher/chgcourse$",api_teacher.api_teacher_chgcourse),

    url(r"^admin/judgecourse",api_admin.api_admin_judge),
    url(r"^admin/modifycourse",api_admin.api_admin_modify_course),
    url(r"^admin/modifyteach",api_admin.api_admin_modify_teach),
    url(r"^admin/promote",api_admin.api_admin_promote),
    url(r"^admin/student",api_admin.api_student_info),
    url(r"^admin/teacher",api_admin.api_teacher_info),
    
]
