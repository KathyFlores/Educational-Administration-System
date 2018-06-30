from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse

from basicInfo.models import account, examination, takeup, teach, course, room, learn, master, college,student,teacher,readyteach
import datetime,time,re
import traceback
from django.db.models import Q



@csrf_exempt
def api_admin_course(request):
    if request.method=="GET":
        '''
            id(string):课程号
            name(string):课程名称
            credit(float):课程学分
            hour(float):课程课时
            intro(string):课程介绍
            semester(string):课程学期
        '''

        allret=[]
        waitCourses=course.objects.filter(type="0")
        for waitcourse in waitCourses:
            ret={}
            ret["id"]=str(waitcourse.course_id)
            ret["name"]=str(waitcourse.name)
            ret["credit"]=float(waitcourse.credit)
            ret["hour"]=float(waitcourse.hour)
            ret["intro"]=str(waitcourse.intro)
            ret["semester"]=str(waitcourse.semester)
            allret.append(ret)
        sorted(allret, key=lambda x: int(x["id"]))
        return JsonResponse(allret,safe=False)
    else:
        '''
        courseid(string):课程号
        examdate(date):考试时间
        permit(bool):是否同意 0:不同意 1:同意
        :type(string)

        '''
        ret = {"success": 0,
               "reason": None
               }
        try:
            courseId=request.POST["courseid"]
            examDate=request.POST["examdate"]
            permit=int(request.POST["permit"])
            type=request.POST["type"]

            if permit:
                try:
                    course_t=course.objects.get(course_id=courseId)
                    if course_t.type!="0":
                        ret["reason"] = "该课程已审批"
                        return JsonResponse(ret)
                    if re.match(r"^[M|C|S]*$",type)==None:
                        return JsonResponse({"success":0,"reason":"课程类型不符合"})
                    course_t.type=type
                    course_t.exam_date=datetime.datetime.strptime(examDate,"%Y-%m-%dT%H:%M")
                    course_t.save()
                    ret["success"]=1
                    return JsonResponse(ret)
                except:
                    ret["reason"] = "没有这门课程"
                    return JsonResponse(ret)
                    pass
            else:
                try:
                    course_t=course.objects.get(course_id=courseId)
                    if course_t.type!="0":
                        ret["reason"] = "该课程已审批"
                        return JsonResponse(ret)
                    course_t.delete()
                    ret["success"]=1
                    return JsonResponse(ret)
                except:
                    ret["reason"] = "没有这门课程"
                    return JsonResponse(ret)
        except Exception as e:
            print(e)
            traceback.print_exc()
            ret["reason"] = "批准失败"
            return JsonResponse(ret)




@csrf_exempt
def api_admin_teach(request):

    if request.method=="GET":
        try:
            allret=[]
            wait_courses=readyteach.objects.all()
            for wait_course in wait_courses:
                '''
                course(string):课程代码
                course_name
                tid(string):教师工号
                capacity(string):课程容量
                name(string)
                '''
                print("------")
                ret = {}
                ret["course"]=str(wait_course.course_id.course_id)

                ret["tid"]=str(wait_course.teacher_id.teacher_id.account_id)
                ret["capacity"]=str(wait_course.capacity)
                ret["name"]=str(wait_course.teacher_id.name)
                ret["course_name"]=wait_course.course_id.name
                allret.append(ret)
            sorted(allret,key=lambda x:int(x["course"]))
            return JsonResponse(allret,safe=False)
        except Exception as e:
            print(e)
            traceback.print_exc()
            return JsonResponse([],safe=False)
    else:
        '''
        course(string):课程代码
        tid(string):教师工号
        capacity(string):课程容量
        permit(bool):是否同意 0:不同意 1:同意
        '''
        course_id = request.POST["course"]
        teacher_id = request.POST["tid"]
        capacity=request.POST["capacity"]
        permit=int(request.POST["permit"])
        ret = {"success": 0,
               "reason": None
        }
        if permit:

            try:
                waitCourses = readyteach.objects.filter(course_id=course_id, teacher_id=teacher_id)
                teachList=teach.objects.filter(course_id=course_id,teacher_id=teacher_id)
                for waitCourse in waitCourses:
                    teachobj = teach()
                    teachobj.course_id = waitCourse.course_id
                    teachobj.teacher_id = waitCourse.teacher_id
                    teachobj.capacity = capacity
                    teachobj.duplicate=len(teachList)+1
                    teachobj.save()
                    waitCourse.course_id.duplicate += 1
                    waitCourse.course_id.save()
                    waitCourse.delete()
                    break
                ret["success"] = 1

                return JsonResponse(ret)
            except Exception as e:
                print(e)
                traceback.print_exc()
                ret["reason"] = "没有改课"
                return JsonResponse(ret)
        else:
            try:
                waitCourses = readyteach.objects.filter(course_id=course_id, teacher_id=teacher_id)
                for waitCourse in waitCourses:
                    waitCourse.delete()
                    break
                ret["success"] = 1

                return JsonResponse(ret)
            except Exception as e:
                print(e)
                traceback.print_exc()
                ret["reason"] = "没有改课"
                return JsonResponse(ret)


@csrf_exempt
def api_admin_courseAccepted_id_list(request):
    if request.method=="GET":
        allret=[]
        courses=course.objects.filter(~Q(type ="0"))
        for course_t in courses:
            allret.append(
                {"course_id":course_t.course_id}
            )
        return JsonResponse(allret,safe=False)
    return HttpResponseBadRequest()

@csrf_exempt
def api_admin_courseAccepted(request):
    if request.method=="POST":
        return api_admin_modify_course(request)

    else:
        '''
        @param
            course_id(string): 课程的id
        @return
            json object{
                course_id(string): 课程的id
                name(string): 课程的名字
                credit(real): 课程学分
                hour(read): 课程学时
                type(string): 课程类型
                intro(string):课程介绍
                exam_date(string): 考试时间
                "teachList":(array)json object{
                    teach_id(string): 开课id
                }
            }
        '''
        ret={
            "course_id":None,
            "name":None,
            "credit":None,
            "hour":None,
            "type":None,
            "intro":None,
            'exam_date':None,
            "teachList":[]
        }
        try:
            courseId=request.GET["course_id"]

            course_t=course.objects.get(course_id=courseId)
            ret["course_id"]=courseId
            ret["name"]=course_t.name
            ret["credit"]=float(course_t.credit)
            ret["hour"]=float(course_t.hour)
            ret["type"]=course_t.type
            ret["intro"]=course_t.intro
            if course_t.exam_date:
                ret["exam_date"]=course_t.exam_date.strftime("%Y-%m-%d %H:%M")

            teachList=teach.objects.filter(course_id=courseId)
            for teach_t in teachList:
                print("-----")
                ret["teachList"].append(
                    {"teach_id":teach_t.teach_id}
                )
            return  JsonResponse(ret,safe=False)

        except Exception as e:
            print(e)
            traceback.print_exc()
            return JsonResponse(ret)


def api_admin_teachAccepted(request):
    if request.method=="POST":
        '''
            @param
                teach_id(string): teach的id
                tid(string): 老师工号
                capacity(string):课程容量
            @return
                json object{
                    success(bool):操作成功与否
                    reason(string):不成功的原因
                }
        '''
        ret = {"success": 0,
               "reason": None
               }
        try:
            teach_id=request.POST["teach_id"]
            tid=request.POST["tid"]
            capacity=request.POST["capacity"]
            teach_t=teach.objects.get(teach_id=teach_id)
            teach_t.teacher_id=teacher.objects.get(teacher_id=tid)
            teach_t.capacity=capacity
            teach_t.save()
            ret["success"]=1
            return JsonResponse(ret)

        except Exception as e:
            print(e)
            traceback.print_exc()
            ret["reason"]="修改失败"
            return JsonResponse(ret)
    else:
        '''
            @param
                teach_id(string): teach的id
            @return
                json object{
                    teach_id(string): 开课id
                    tid(string): 老师工号
                    capacity(string):课程容量
                }
        '''
        ret={
            "teach_id":None,
            "tid":None,
            "capacity":None
        }
        try:
            teach_id=request.GET["teach_id"]
            teach_t=teach.objects.get(teach_id=teach_id)
            ret["teach_id"]=teach_id
            ret["tid"]=teach_t.teacher_id.teacher_id.account_id
            ret["capacity"]=teach_t.capacity
            return JsonResponse(ret)
        except Exception as e:
            print(e)
            traceback.print_exc()
            return JsonResponse(ret)












@csrf_exempt
def api_admin_modify_course(request):
    if request.method == "POST":
        try:
            id = request.POST["id"]

            name = request.POST["name"]
            hour=request.POST["hour"]
            credit = request.POST["credit"]
            intro = request.POST["intro"]
            type = request.POST["type"]
            examDate=request.POST["exam_date"]
            if re.match("^[M|C|S]*$",type)==None:
                return JsonResponse({"success":0,"reason":"课程类型不符合要求"})

            tmp_course = course.objects.get(course_id=id)
            tmp_course.name = name
            tmp_course.hour=hour
            tmp_course.credit = credit
            tmp_course.intro = intro
            tmp_course.type = type
            print(tmp_course.exam_date)

            tmp_course.exam_date=datetime.datetime.strptime(examDate,"%Y-%m-%dT%H:%M")
            #tmp_course.exam_date.strptime()
            #tmp_course.exam_date= datetime.datetime(2018,1,1,11,20)
            tmp_course.save()

            # a=tmp_course.exam_date.strftime("%Y-%m-%d %H:%M")
            # print(a)
            return JsonResponse({"success": 1, "reason": None})

        except Exception as e:
            print(e)
            traceback.print_exc()
            return JsonResponse({"success": 0, "reason": "修改失败"})
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
            return JsonResponse({"success": 0, "reason": "没有这个学生"})
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
            return JsonResponse({"success": 0, "reason": "没有这个老师"})
    return HttpResponseBadRequest()


