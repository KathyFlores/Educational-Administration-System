from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse

from basicInfo.models import account, examination, takeup, teach, course, room, learn, student,attrib,major,discipline
import traceback


@csrf_exempt
def api_student_info(request):
    if request.method == "GET":
        try:
            print("----")
            account_id = request.GET["account_id"]

            student_info=student.objects.get(student_id=account_id)

            student_attrib_info=attrib.objects.get(account_id=account_id)

            major_info=major.objects.get(student_id=account_id)
            dis_id=major_info.discipline_id

            dis_info=discipline.objects.get(discipline_id=dis_id)




            ret={}

            ret["name"]=student_info.name
            ret["nick"]=student_attrib_info.nickname
            ret["major"]=dis_info.name
            ret["grade"]=student_info.grade
            ret["email"]=student_attrib_info.email
            ret["dorm"]=student_info.dorm




            return JsonResponse(ret)

        except Exception as e:
            print(e)
            ret = {}

            ret["name"] = "获取失败"
            ret["nick"] = "获取失败"
            ret["major"] = "获取失败"
            ret["grade"] = "获取失败"
            ret["email"] = "获取失败"
            ret["dorm"] = "获取失败"
            return JsonResponse(ret)
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
                takeup_id = e.takeup_id
                teach_id = takeup_id.teach_id
                course_id = teach_id.course_id
                tmp["name"] = course_id.name
                if course_id.exam_date:
                    tmp["time"] = course_id.exam_date.strftime("%Y-%m-%d %H:%M")
                else:
                    continue
                room_id = takeup_id.room_id
                tmp["room"] = room_id.location
                tmp["seat"] = e.position
                exam_list.append(tmp)

            return JsonResponse(exam_list,safe=False)

        except Exception as e:
            print(e)
            traceback.print_exc()
            return JsonResponse([], safe=False)
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
                course_id = l.course_id
                tmp["name"] = course_id.name
                tmp["credit"] = course_id.credit
                tmp["grade"] = l.grade
                tmp["course_id"]=l.course_id.course_id
                if l.grade!=None:
                    course_list.append(tmp)

            return JsonResponse(course_list,safe=False)

        except Exception as e:
            print(e)
            traceback.print_exc()
            return JsonResponse([], safe=False)
    return HttpResponseBadRequest()

