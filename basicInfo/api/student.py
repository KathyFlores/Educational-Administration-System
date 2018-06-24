from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse

from basicInfo.models import account, examination, takeup, teach, course, room, learn, student,attrib,major,discipline

@csrf_exempt
def api_student_info(request):
    if request.method == "GET":
        try:
            account_id = request.GET["account_id"]

            student_info=student.objects.get(student_id=account_id)

            student_attrib_info=attrib.objects.get(student_id=account_id)

            major_info=major.objects.get(studnet_id=account_id)
            dis_id=major_info["discipline_id"]

            dis_info=discipline.objects.get(discipline_id=dis_id)



            ret={}

            ret["name"]=student_info["name"]
            ret["nick"]=student_attrib_info["nickname"]
            ret["major"]=dis_info["name"]
            ret["grade"]=student_info["grade"]
            ret["email"]=student_attrib_info["email"]




            return JsonResponse(ret)

        except:
            return HttpResponseBadRequest()

@csrf_exempt
def api_student_exam(request):
    if request.method == "GET":
        try:
            account_id = request.GET["account_id"]

            exam = examination.objects.filter(student_id=account_id)

            exam_list = []
            for e in exam:
                tmp = {}
                takeup_id = takeup.objects.get(id=e.takeup_id)
                teach_id = teach.objects.get(id=takeup_id.teach_id)
                course_id = course.objects.get(course_id=teach_id.course_id)
                tmp["name"] = course_id.name
                tmp["time"] = teach_id.exam_date
                room_id = room.objects.get(room_id=takeup_id.room_id)
                tmp["room"] = room_id.location
                tmp["seat"] = e.position
                exam_list.append(tmp)

            return JsonResponse(exam_list)

        except:
            return HttpResponseBadRequest()

@csrf_exempt
def api_student_grade(request):
    if request.method == "GET":
        try:
            account_id = request.GET["account_id"]

            student_learn = learn.objects.filter(student_id=account_id)

            course_list = []
            for l in student_learn:
                tmp = {}
                course_id = course.objects.get(course_id=l.course_id)
                tmp["name"] = course_id.name
                tmp["credit"] = course_id.credit
                tmp["grade"] = l.grade
                if l.grade!=None:
                    course_list.append(tmp)

            return JsonResponse(course_list)

        except:
            return HttpResponseBadRequest()

