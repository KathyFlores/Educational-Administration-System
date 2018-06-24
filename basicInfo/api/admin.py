from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse

from basicInfo.models import account, examination, takeup, teach, course, room, learn, master, college,student,teacher

@csrf_exempt
def api_admin_suspend(request):
    if request.method == "GET":
        try:
            course_list = course.objects.filter(student_id=account_id)

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

@csrf_exempt
def api_admin_judge(request):
    if request.method == "POST":
        try:
            id = request.POST["id"]
            accept = request.POST["accept"]

            tmp_course = course.objects.get(course_id=id)
            if accept:
                tmp_course.type = "普通课程"
                tmp_course.save()

                duplicate=request.POST["duplicate"]
                teachers=request.POST["teacher"]
                exam=request.POST["exam"]
                capacitys=request.POST["capacity"]
                for i in range(duplicate):
                    teach_ele=teach()
                    teach_ele.duplicate=duplicate
                    teach_ele.capacity=capacitys[i]
                    teach_ele.teacher_id=teachers[i]
                    teach_ele.exam_date=exam
                    teach_ele.course_id_id=id
                    teach_ele.save()

            else:
                tmp_course.delete()
            return JsonResponse({"success": 1, "reason": None})

        except:
            return HttpResponseBadRequest()

@csrf_exempt
def api_admin_modify_course(request):
    if request.method == "POST":
        try:
            pre_id = request.POST["pre_id"]
            post_id=request.POST["post_id"]

            name = request.POST["name"]
            credit = request.POST["credit"]
            intro = request.POST["intro"]
            type = request.POST["type"]

            if pre_id==post_id:
                tmp_course = course.objects.get(course_id=pre_id)
            else:
                tmp_course=course.objects.get(course_id=pre_id)
                tmp_course.delete()
                tmp_course=course()
                tmp_course.course_id_1=post_id
            tmp_course.name = name
            tmp_course.credit = credit
            tmp_course.intro = intro
            tmp_course.type = type
            tmp_course.save()
            return JsonResponse({"success": 1, "reason": None})

        except:
            return HttpResponseBadRequest()

@csrf_exempt
def api_admin_modify_teach(request):
    if request.method == "POST":
        try:
            id = request.POST["teach_id"]

            teacher=request.POST["teacher"]

            capacity=request.POST["capacity"]

            teach_info=teach.objects.get(teach_id=id)
            teach_info.capacity=capacity
            teach_info.teacher_id=teacher
            teach_info.save()

            return JsonResponse({"success": 1, "reason": None})

        except:
            return HttpResponseBadRequest()

@csrf_exempt
def api_admin_promote(request):
    if request.method == "POST":
        try:
            account_id = request.POST["account_id"]
            college_name = request.POST["college"]

            new_master = master()
            new_master.teacher_id = account_id
            new_master.college_id = college.objects.get(name=college_name)
            new_master.save()
            teacher_info=teacher.objects.get(teacher_id=account_id)
            teacher_info.management=college_name
            teacher_info.save()

            return JsonResponse({"success": 1, "reason": None})

        except:
            return HttpResponseBadRequest()

@csrf_exempt
def api_student_info(request):
    if request.method == "POST":
        try:
            account_id = request.POST["account_id"]
            name=request.POST["name"]
            dorm=request.POST["dorm"]

            info=student.objects.get(student_id=account_id)
            info.name = name
            info.dorm = dorm
            info.save()

            return JsonResponse({"success": 1, "reason": None})

        except:
            return HttpResponseBadRequest()

@csrf_exempt
def api_teacher_info(request):
    if request.method == "POST":
        try:
            account_id = request.POST["account_id"]
            name=request.POST["name"]
            title=request.POST["title"]
            office=request.POST["office"]
            management=request.POST["management"]

            info=teacher.objects.get(teacher_id=account_id)
            info.name = name
            info.title = title
            info.office = office
            info.management = management
            info.save()

            return JsonResponse({"success": 1, "reason": None})

        except:
            return HttpResponseBadRequest()


