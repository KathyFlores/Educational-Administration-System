from basicInfo.models import course, major, discipline, teacher
from django.utils import timezone
import datetime

def search(post, courses):
    if post['search_content']:
        search_type = post['search_type']
        if(post['search_field'] == 'course_name'):
            course_name = post['search_content']
            if search_type == 'equal':
                courses = course.objects.all().filter(name__iexact=course_name)
            elif search_type == 'contain':
                courses = course.objects.all().filter(name__icontains=course_name)
            elif search_type == 'exclude':
                courses = course.objects.all().exclude(name__iexact=course_name)
        elif post['search_field'] == 'course_id':
            try:
                course_id = int(post['search_content'])
            except: course_id = 0
            if search_type == 'equal':
                courses = course.objects.all().filter(course_id__iexact=course_id)
            elif search_type == 'contain':
                courses = course.objects.all().filter(course_id__icontains=course_id)
            elif search_type == 'exclude':
                courses = course.objects.all().exclude(course_id__iexact=course_id)
        elif post['search_field'] == 'teacher_name':
            teacher_name = post['search_content']
            if search_type == 'equal':
                teachers = teacher.objects.filter(name__iexact=teacher_name)
            elif search_type == 'contain':
                teachers = teacher.objects.filter(name__icontains=teacher_name)
            elif search_type == 'exclude':
                teachers = teacher.objects.exclude(name__iexact=teacher_name)
            for teacher in teachers:
                courses = courses.filter(college_id_1__takeup__teacher_id = teacher)
    return courses

def getDisciplineByStudent(student_id):
    major = major.objects.get(student_id=student_id)
    discipline_id = major.discipline_id
    return discipline.objects.get(discipline_id=discipline_id)

def timestampToDatetime(ts):
    if isinstance(ts, (int, float, str)):
        try:
            ts = int(ts)
        except ValueError:
            raise
        if len(str(ts)) == 13:
            ts = int(ts / 1000)
        if len(str(ts)) != 10:
            raise ValueError
    else:
        raise ValueError()
    return datetime.datetime.fromtimestamp(ts,tz=timezone.utc)