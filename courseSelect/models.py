from django.db import models
from basicInfo.models import student, teacher, course, discipline, takeup, teach, time
# Create your models here.

# 选课信息
class selection(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE) # ref Student, 学生
    teach = models.ForeignKey(teach, on_delete=models.CASCADE) # ref Teach, 排课信息
    select_time = models.DateTimeField(null=True) # 选课时间
    priority = models.IntegerField() # 优先级
    state = models.BooleanField() # 选课状态，即是否选上

# 培养方案
class curriculum(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE) # ref Student, 学生
    courses = models.ManyToManyField(course, related_name='course_curriculum', null=True) # ref Course, 课程
   
class requiredCourse(models.Model):
    discipline = models.ForeignKey(discipline, on_delete=models.CASCADE)
    required_courses = models.ManyToManyField(course, related_name='required_course', null=True)

class creditNeed(models.Model):
    discipline = models.ForeignKey(discipline, on_delete=models.CASCADE, unique=True) # ref Major, 专业
    elective = models.FloatField() # 选修课最低学分要求
    public = models.FloatField() # 公共课最低学分要求

class timeSlot(models.Model):
    start = models.DateTimeField(null=False)
    end = models.DateTimeField(null=False)

class selectControl(models.Model):
    first_time = models.ForeignKey(timeSlot, related_name='first_time', on_delete=models.CASCADE)
    apply_time = models.ForeignKey(timeSlot, related_name='apply_time', on_delete=models.CASCADE)
    withdraw_time = models.ForeignKey(timeSlot, on_delete=models.CASCADE)
    max_connections = models.IntegerField(default=500)