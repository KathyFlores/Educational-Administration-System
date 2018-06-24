from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse

from basicInfo.models import account, examination, takeup, teach, course, room, learn, teacher, student,attrib
from datetime import time

@csrf_exempt
def api_teacher_info(request):
    if request.method == "GET":
        try:
            print("------")
            account_id = request.GET["account_id"]
            print(account_id)

            teacher_info=teacher.objects.get(teacher_id=account_id)

            print(teacher_info)

            teacher_attrib_info=attrib.objects.get(account_id=account_id)
            print(teacher_attrib_info)

            ret={}
            ret["name"]=teacher_info.name
            print(ret)
            ret["teacher_title"]=teacher_info.title
            ret["teacher_office"]=teacher_info.office
            ret["teacher_management"]=teacher_info.management
            ret["email"]=teacher_attrib_info.email

            return JsonResponse(ret)

        except:
            return HttpResponseBadRequest()
    else:
        print("fuck")
        ret={}
        try:
            account_id=request.POST["account_id"]
            account_email=request.POST["account_email"]
            teacher_office=request.POST["teacher_office"]

            teacher_info = teacher.objects.get(teacher_id=account_id)
            teacher_attrib_info = attrib.objects.get(account_id=account_id)

            print(teacher_info,teacher_attrib_info)
            teacher_info.office=teacher_office
            teacher_attrib_info.email=account_email
            teacher_info.save()
            teacher_attrib_info.save()
            ret["success"]=1
            ret["reason"]=None
            return JsonResponse(ret)
        except:
            ret["success"] = 0
            ret["reason"] = "信息不符合要求"
            return JsonResponse(ret)





@csrf_exempt
def api_teacher_course(request):
    if request.method == "GET":
        print("=====")
        try:
            account_id = request.GET["account_id"]
            print(account_id)
            #teacher_course=teach.objects.get(teacher_id=account_id)
            teacher_course=teach.objects.filter(teacher_id=account_id)
            print(teacher_course)
            course_list=[]
            for t in teacher_course:
                tmp={}
                print(t.course_id.course_id)
                course_id=t.course_id
                tmp["teach_id"]=t.teach_id
                tmp["hour"]=course_id.hour
                tmp["name"]=course_id.name
                tmp["credit"]=course_id.credit
                tmp["intro"] = course_id.intro
                print(t.teach_id,"*****")

                try:
                    takeup_info=takeup.objects.get(teach_id=t.teach_id)
                except:
                    tmp["time"]=None
                    tmp["room"]=None
                    course_list.append(tmp)
                    continue


                # takeup_info.time_id.start=time(4,7,1,10)
                # takeup_info.time_id.end = time(4, 7, 1, 10)
                # takeup_info.time_id.save()

                print("-----", takeup_info.time_id.start)
                tmp["time"]=str(takeup_info.time_id.start.strftime("%H:%M"))

                tmp["time"]+=" - "+str(takeup_info.time_id.end.strftime("%H:%M"))
                print(tmp["time"])
                tmp["room"]=takeup_info.room_id.location
                print(tmp["room"])
                course_list.append(tmp)

            return JsonResponse(course_list,safe=False)

        except Exception as e:
            print(e)
            return HttpResponseBadRequest()

@csrf_exempt
def api_teacher_addcourse(request):
    if request.method == "POST":
        try:
            id = request.POST["id"]
            name = request.POST["name"]
            credit = request.POST["credit"]
            intro = request.POST["intro"]
            hour=float(request.POST["hour"])

            try:
                new_course=course.objects.get(course_id=id)
                return JsonResponse({"success": 0, "reason": "课程已存在"})
            except:
                pass


            new_course = course()
            new_course.course_id = id
            new_course.name = name
            new_course.credit = credit
            new_course.intro = intro
            new_course.hour=hour
            new_course.type=0
            new_course.save()
            return JsonResponse({"success": 1, "reason": None})

        except:
            return HttpResponseBadRequest()

@csrf_exempt
def api_teacher_chgcourse(request):
    if request.method == "POST":
        try:
            account_id=request.POST["account_id"]

            id = request.POST["id"]

            intro = request.POST["intro"]

            try:


                tmp_course=course.objects.get(course_id=id)

                _=teach.objects.filter(teacher_id=account_id,course_id=id)
                if len(_)<1:
                    return JsonResponse({"success": 0, "reason": "不能修改您未开设的课程"})


                tmp_course.intro = intro
                tmp_course.save()
                return JsonResponse({"success": 1, "reason": None})
            except:
                return JsonResponse({"success": 0, "reason": "没有相应的课程"})
        except:
            return HttpResponseBadRequest()
