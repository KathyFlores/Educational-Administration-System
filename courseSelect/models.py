from django.db import models
from basicInfo.models import student as Student, teacher as Teacher, course as Course, discipline as Discipline, takeup as Takeup, teach as Teach
# Create your models here.

# 选课信息
class Selection(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE) # ref Student, 学生
    teach = models.ForeignKey(Teach, on_delete=models.CASCADE) # ref Teach, 排课信息
    select_time = models.DateTimeField(null=True) # 选课时间
    priority = models.IntegerField() # 优先级
    state = models.BooleanField() # 选课状态，即是否选上

# 培养方案
class Curriculum(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE) # ref Student, 学生
    courses = models.ManyToManyField(Course, related_name='course_curriculum', null=True) # ref Course, 课程
   
class RequiredCourse(models.Model):
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    required_courses = models.ManyToManyField(Course, related_name='required_course', null=True)

class CreditNeed(models.Model):
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, unique=True) # ref Major, 专业
    elective = models.FloatField() # 选修课最低学分要求
    public = models.FloatField() # 公共课最低学分要求

class TimeSlot(models.Model):
    start = models.DateTimeField(null=False)
    end = models.DateTimeField(null=False)

class SelectControl(models.Model):
    first_time = models.ForeignKey(TimeSlot, related_name='first_time', on_delete=models.CASCADE)
    apply_time = models.ForeignKey(TimeSlot, related_name='apply_time', on_delete=models.CASCADE)
    withdraw_time = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    max_connections = models.IntegerField(default=500)