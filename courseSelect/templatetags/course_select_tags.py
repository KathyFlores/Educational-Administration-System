from django import template
from django.db.models import Max
from courseSelect.models import Curriculum, Selection, SelectControl
from basicInfo.models import course as Course, teach as Teach, teacher as Teacher, takeup as Takeup, room as Room, time as Time, student as Student, discipline as Discipline, major as Major
import django.utils.timezone as timezone
import pytz
import datetime
register = template.Library()

@register.assignment_tag
def getSectionByCourse(course_id):
    return Teach.objects.filter(course_id=Course.objects.get(course_id=course_id)).distinct()
#     return Category.objects.all()
@register.assignment_tag
def getTeacherBySection(section_id):
    return Teacher.objects.filter(takeup__teach_id=Teach.objects.get(teach_id=section_id)).distinct()

@register.assignment_tag
def getRoomBySection(section_id):
    return Room.objects.filter(takeup__teach_id=Teach.objects.get(teach_id=section_id)).distinct()

@register.assignment_tag
def getTimeBySection(section_id):
    return Time.objects.filter(takeup__teach_id=Teach.objects.get(teach_id=section_id)).distinct()


@register.simple_tag
def getCapacityBySection(section_id):
    return Teach.objects.get(teach_id=section_id).capacity

@register.assignment_tag
def getCourseBySection(section_id):
    course = Teach.objects.get(teach_id=section_id).course_id
    return course

@register.assignment_tag
def getStudentBySection(section_id):
    return Student.objects.filter(selection__teach = Teach.objects.get(teach_id=section_id),selection__state=True)

@register.simple_tag
def getMajorByStudent(student_id):
    major = Major.objects.get(student_id=student_id)
    discipline_id = major.discipline_id
    return Discipline.objects.get(discipline_id=discipline_id).name

@register.filter
def isInCurriculum(student, course):
    if(course in Curriculum.objects.get(student=student).courses.all()):
        return 1
    else:
        return 0

@register.filter
def isSelect(student, section):
    
    if(section in Teach.objects.filter(takeup__teach_id__selection__student=student)):
        return 1
    else:
        return 0
@register.filter
def isSelectStateTrue(student, section):
    selection = Selection.objects.get(student=student,teach=section)
    return selection.state
# return 1

@register.simple_tag
def getTimestampByDate(date):
    return int(date.timestamp())

@register.assignment_tag
def isSelectTime():
    now = timezone.now()
    select_control = SelectControl.objects.all().order_by('-pk')[:1][0]
    if now > select_control.first_time.start and now < select_control.first_time.end:
        return True
    elif now > select_control.apply_time.start and now < select_control.apply_time.end:
        return True
    else:
        return False

@register.assignment_tag
def isQuitTime():
    now = timezone.now()
    select_control = SelectControl.objects.all().order_by('-pk')[:1][0]
    if now > select_control.first_time.start and now < select_control.first_time.end:
        return True
    elif now > select_control.apply_time.start and now < select_control.apply_time.end:
        return True
    elif now > select_control.withdraw_time.start and now < select_control.withdraw_time.end:
        return True
    else:
        return False
# @register.filter
# def enrolled(user, course):
#     if(TriedCourse.objects.filter(user=user, course=course)):
#         return True
#     else:
#         return False