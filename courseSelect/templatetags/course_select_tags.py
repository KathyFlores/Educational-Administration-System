from django import template
from django.db.models import Max
from courseSelect.models import curriculum, selection, selectControl
from basicInfo.models import course, teach, teacher, takeup, room, time, student, discipline, major
import django.utils.timezone as timezone
import pytz
import datetime
register = template.Library()

@register.assignment_tag
def getSectionByCourse(course_id):

    return teach.objects.filter(course_id=course.objects.get(course_id=int(course_id))).distinct()
#     return Category.objects.all()
@register.assignment_tag
def getTeacherBySection(section_id):
    return teacher.objects.filter(takeup__teach_id=teach.objects.get(teach_id=int(section_id))).distinct()

@register.assignment_tag
def getRoomBySection(section_id):
    return room.objects.filter(takeup__teach_id=teach.objects.get(teach_id=int(section_id))).distinct()

@register.assignment_tag
def getTimeBySection(section_id):
    return time.objects.filter(takeup__teach_id=teach.objects.get(teach_id=int(section_id))).distinct()


@register.simple_tag
def getCapacityBySection(section_id):
    return teach.objects.get(teach_id=int(section_id)).capacity

@register.assignment_tag
def getCourseBySection(section_id):
    course = teach.objects.get(teach_id=int(section_id)).course_id
    return course

@register.assignment_tag
def getStudentBySection(section_id):
    return student.objects.filter(selection__teach = teach.objects.get(teach_id=int(section_id)),selection__state=True)

@register.simple_tag
def getMajorByStudent(student_id):
    major = major.objects.get(student_id=student_id)
    discipline_id = major.discipline_id
    return discipline.objects.get(discipline_id=discipline_id).name

@register.filter
def isInCurriculum(student, course):
    if(course in curriculum.objects.get(student=student).courses.all()):
        return 1
    else:
        return 0

@register.filter
def isSelect(student, section):
    
    if(section in teach.objects.filter(takeup__teach_id__selection__student=student)):
        return 1
    else:
        return 0
@register.filter
def isSelectStateTrue(student, section):
    selection = selection.objects.get(student=student,teach=section)
    return selection.state
# return 1

@register.simple_tag
def getTimestampByDate(date):
    return int(date.timestamp())

@register.assignment_tag
def isSelectTime():
    now = timezone.now()
    select_control = selectControl.objects.all().order_by('-pk')[:1][0]
    if now > select_control.first_time.start and now < select_control.first_time.end:
        return True
    elif now > select_control.apply_time.start and now < select_control.apply_time.end:
        return True
    else:
        return False

@register.assignment_tag
def isQuitTime():
    now = timezone.now()
    select_control = selectControl.objects.all().order_by('-pk')[:1][0]
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