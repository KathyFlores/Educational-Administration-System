from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse

from basicInfo.models import account, attrib, teacher,student

import hashlib as hash, json, time, random,re

basicUrl="http://127.0.0.1:8000/static/basicInfo/"


@csrf_exempt
def api_account_post(request):

    if request.method == "POST":
        print("log in")
        username = request.POST["account_id"]
        password = request.POST["account_pw"]
        print(username, password)

        try:
            obj = account.objects.get(account_id=username)
            print("----")
            passwd = obj.password
            salt = obj.salt
            passwordAfter = hash.sha512((hash.sha512(password.encode()).hexdigest() + salt).encode()).hexdigest()
            print(passwd, passwordAfter)
            if passwordAfter == passwd:
                request.session["account_id"] = username
                request.session["type"]=int(obj.type)

                return JsonResponse({"success": 1, "type": obj.type, "reason": None})

            else:
                return JsonResponse({"success": 0, "type": None, "reason": '密码错误'})

        except:
            print("===")
            return JsonResponse({"success": 0, "type": None, "reason": '用户名错误'})

    return HttpResponseBadRequest()


@csrf_exempt
def api_account_register_post(request):
    print("regist")
    if request.method == "POST":
        username = request.POST.get("account_id", '')
        password = request.POST.get("account_pw", '')

        type = request.POST.get("accout_type", 0)

        print(username, password, type)



        if (len(password) < 6 or len(password) > 10):
            return JsonResponse({
                "success": 0,
                "reason": "密码长度必须大于5位小于13位"
            })
        if re.match(r"^[0-9]*$",password)!=None:
            return JsonResponse({
                "success":0,
                "reason":"密码不能全部由数字组成"
            })
        if re.match(r"^[0-9|a-z|A-Z]*$",password)==None:
            return JsonResponse({
                "success":0,
                "reason":"密码必须由6-12位数字、字母"
            })

        if len(username) < 6:
            return JsonResponse({
                "success": 0,
                "reason": "用户名短于6位"
            })
        try:
            account.objects.get(account_id=username)
            return JsonResponse({
                "success": 0,
                "reason": "用户名已存在"
            })
        except:
            salt1 = int(time.time() % 100)
            salt = "00" if salt1 == 0 else str(salt1)
            for i in range(6):
                salt += str(
                    hex(int(random.uniform(0, 16)))
                )[2:3]

            print(salt)
            passwordAfter = hash.sha512((hash.sha512(password.encode()).hexdigest() + salt).encode()).hexdigest()
            account_info=account.objects.create(account_id=username, password=passwordAfter, salt=salt)
            print(account_info)

            attrib.objects.create(account_id=account_info, nickname=username, picture="null",
                                  email=username + "@zju.edu.cn", exp=0, coin=0)
            if account_info.type==0:
                student_info=student()
                student_info.student_id=account_info.account_id
                student_info.name="用户"
                student_info.save()
            elif account_info.type==1:
                teacher_info=teacher()
                teacher_info.teacher_id=account_info
                teacher_info.name="用户"
                teacher_info.office="Null"
                teacher_info.save()


            request.session["account_id"] = username
            return JsonResponse({
                "success": 1,
                "reason": None,
            })
    return HttpResponseBadRequest()


@csrf_exempt
def api_account_repassword_post(request):
    '''
    ##### POST /api/account/repassword

    账户密码修改

    ```doc
    @param
        account_id(string):当前的用户名
        account_pw(string):新建的密码
    @return
        json object{
            success(bool):修改成功与否
            reason(string):不成功的原因
        }
    ```
    :param request:
    :return:
    '''

    if request.method == "POST":
        account_id = request.POST.get("account_id", "")
        account_pw = request.POST.get("account_pw", "")
        try:
            obj = account.objects.get(account_id=account_id)
            if (len(account_pw) < 6 or len(account_pw) > 18):
                return JsonResponse({
                    "success": 0,
                    "reason": "密码长度不符合要求"
                })

            salt1 = int(time.time() % 100)
            salt = "00" if salt1 == 0 else str(salt1)
            for i in range(6):
                salt += str(
                    hex(int(random.uniform(0, 16)))
                )[2:3]

            print(salt)
            passwordAfter = hash.sha512((hash.sha512(account_pw.encode()).hexdigest() + salt).encode()).hexdigest()
            obj.password = passwordAfter
            obj.save()
            return JsonResponse({
                "success": 1,
                "reason": None
            })

        except:
            return HttpResponseNotFound()


@csrf_exempt
def api_account_person_post(request):
    try:
        account_id = request.POST["account_id"]
        nick = request.POST["nick"]
        email = request.POST["email"]
        exp = int(request.POST["exp"])
        coin = int(request.POST["coin"])

        print(account_id,nick,email,exp,coin)

        obj = attrib.objects.get(account_id=account_id)
        obj.nickname=nick
        obj.email=email

        print(obj.nickname)

        print(1)

        if(exp>0):
            obj.exp=exp
        if(coin>0):
            obj.coin=coin
        print(2)
        obj.save()
        return JsonResponse({"success": 1, "reason": None})

    except:
        return HttpResponseBadRequest()


@csrf_exempt
def api_account_person_get(request):
    try:
        account_id = request.GET["account_id"]

        obj = attrib.objects.get(account_id=account_id)


        return JsonResponse(
            {
                "nick": obj.nickname,
                "email": obj.email,
                "exp": obj.exp,
                "coin": obj.coin
            }
        )

    except:
        return HttpResponseBadRequest()


@csrf_exempt
def api_account_person(request):
    if request.method == "POST":
        return api_account_person_post(request)
    else:
        return api_account_person_get(request)

@csrf_exempt
def api_account_img(request):
    if request.method == "POST":
        print("123445")
        account_id=request.POST["account_id"]
        # print(account_id)
        files = request.FILES.get('file')  # 获取图片
        # 图片存放路径
        print(files)
        print(account_id)

        attrib_info=attrib.objects.get(account_id=account_id)
        attrib_info.picture=files
        attrib_info.save()

        return JsonResponse({"success": 1, "reason": None})
    else:

        account_id=request.GET["account_id"]
        try:
            attrib_info=attrib.objects.get(account_id=account_id)
        except:
            return JsonResponse({"success": 0, "image": None, "reason": "没有该用户"})
        filename=re.split("/",attrib_info.picture.name)[-1] if attrib_info.picture.name!="null" else "null.jpg"
        url=basicUrl+"picture/"+filename
        return JsonResponse({"success":1,"image":url,"reason":None})

