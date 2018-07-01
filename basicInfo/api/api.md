### API文档

#### Account API

##### POST /api/account/login(finish)

账户登录

```doc
@param
    account_id(string):要查询的用户名
	account_pw(string):要查询的密码
@return
	json object{
		success(bool):登录成功与否
		type(int):该账户的类型（学生、老师、管理员）
		reason(string):不成功的原因
	}
```



##### POST /api/account/register(finish)

账户注册

```doc
@param
	account_id(string):新建的用户名
	account_pw(string):新建的密码
	accout_type(int):注册账户的类型（学生、老师、管理员）
@return
	json object{
		success(bool):注册成功与否
		reason(string):不成功的原因
	}
```



##### POST /api/account/repassword(finish)

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



##### POST /api/account/person

账户信息修改
```doc
@param
	account_id(string):当前的用户名
    nick(string):昵称
    email(string):电子邮箱
    exp(int):个人经验
    coin(int):金币数
@return
	json object{
		success(bool):是否修改成功，
		reason(string):原因
	}
```



##### GET /api/account/person

账户信息查询

```doc
@param
	account_id(string):当前的用户名
@return
	json object{
		nick(string):昵称
		email(string):电子邮箱
		exp(int):个人经验
		coin(int):金币数
	}
```



##### POST /api/account/img

上传头像

```doc
@param
	account_id(string):当前的用户名
	file(img):头像
@return
	json object{
		success(bool):操作成功与否
		reason(string):不成功的原因
	}
```

##### GET /api/account/img

下载图像

返回的是一个可以访问的url:"http://127.0.0.1:8000/static/img/1.jpg"

```doc
@param
    account_id(string):要查询的用户名
@return
	json object{
		success(bool):登录成功与否
		image(String):该学生的头像，如果没有传一个默认图片
		reason(string):不成功的原因
	}
```



#### Student API

##### GET /api/student/info

学生信息查询

```doc
@param
	account_id(string):当前的用户名
@return
	json object{
		name(string):真实姓名
		nick(string):昵称
		major(string):专业
		grade(string):年级
		email(string):邮箱
		dorm(string):寝室
	}
```



##### GET /api/student/exam

学生当前考试查询

```doc
@param
	account_id(string):当前的用户名
@return
	(array) json object{
		name(string):课程名称
		time(time):考试时间
		room(string):考试教室
		seat(int):考试座位
	}
```



##### GET /api/student/grade

学生当前成绩查询

```doc
@param
	account_id(string):当前的用户名
@return
	(array) json object{
		name(string):课程名称
		course_id(string):课程id
		credit(real):课程学分
		grade(int):课程成绩
		
	}
```



#### Teacher API



##### GET /api/teacher/info

教师信息查询

```doc
@param
	account_id(string):当前的用户名
@return
	json object{
		name(string):真实姓名
		teacher_title(string):职称
		teacher_office(string):办公室
		teacher_management(string):管理学院
		email(string):邮箱
		teacher_work(string) college name
	}
```



##### POST /api/teacher/info

教师信息修改
```doc
@param
    	account_id(string):当前的用户名
	account_email(string):邮箱
	teacher_office(string):办公室
@return
	json object{
		success(bool):修改成功与否
		reason(string):不成功的原因
	}
```




##### GET /api/teacher/course (untested)

讲授课程查询

```doc
@param
	account_id(string):上课老师(默认当前用户)
@return
	(array) json object{
		teach_id(int):课程代号
		name(string):课程名称
		credit(real):课程学分
		hour(read):课程学时
		time(time):上课时间
		room(string):上课教室
		intro(string):课程简介
	}
```
##### POST /api/teacher/opencourse

申请开课程

```doc
@param
	account_id(string):当前的用户名
	id(string):课程代号
	capacity(int):课程容量
@return
	json object{
		success(bool):修改成功与否
		reason(string):不成功的原因
	}
```



##### POST /api/teacher/addcourse

申请新增课程

```doc
@param
	id(string):课程代号
	name(string):课程名称
	credit(real):课程学分
	hour(real):课程学时
	intro(string):课程介绍
@return
	json object{
		success(bool):申请成功与否
		reason(string):不成功的原因
	}
```

#### 

##### POST /api/teacher/chgcourse

申请修改课程

```doc
@param
	account_id(string):当前的用户名
	id(string):课程代号
	intro(string):课程介绍
@return
	json object{
		success(bool):修改成功与否
		reason(string):不成功的原因
	}
```



#### Admin API






##### POST /api/admin/promote

教师提升为管理员

```doc
@param
	account_id(string):教师工号
	college(string):学院名称
@return
	json object{
		success(bool):操作成功与否
		reason(string):不成功的原因
	}
```




##### POST /api/admin/student

学生信息修改

```doc
@param
	account_id(string):修改学生用户名
	name(string):真实姓名
	dorm(string):寝室
@return
	json object{
		success(bool):操作成功与否
		reason(string):不成功的原因
	}
```





##### POST /api/admin/teacher

教师信息修改

```doc
@param
	account_id(string):修改教师用户名
    name(string):真实姓名
    title(string):职称
    office(string):办公室
    management(string):管理学院
@return
	json object{
		success(bool):操作成功与否
		reason(string):不成功的原因
	}

```






##### GET /api/admin/course
待审批课程列表

```doc
@param
@return
	(array) json object{
	    {
            id(string):课程号
            name(string):课程名称
            credit(float):课程学分
            hour(float):课程课时
            intro(string):课程介绍
            semester(string):课程学期
		}
	}
```



##### POST /api/admin/course

待审批课程 同意审批

```doc
@param
    courseid(string):课程号
    examdate(date):考试时间
    permit(bool):是否同意 0:不同意 1:同意
@return
	json object{
		success(bool):操作成功与否
		reason(string):不成功的原因
	}
```


###### 

##### GET /api/admin/teach

待审批授课列表

```doc
@param
@return
	(array) json object{
	    {
	    	course(string):课程代码
	    	course_name(string):课程名称
	    	tid(string):教师工号
	    	capacity(string):课程容量
	    	name(string):教师姓名
		}
	}
```



##### POST /api/admin/teach

待审批授课 (不)同意审批

```doc
@param
    course(string):课程代码
    tid(string):教师工号
    capacity(string):课程容量
    permit(bool):是否同意 0:不同意 1:同意
@return
	json object{
		success(bool):操作成功与否
		reason(string):不成功的原因
	}
```








##### GET /api/admin/listCourseAcceptedId
返回所有现在已经通过课程（course）的id

```doc
@param

@return
	(array)json object{
		course_id(string): 每个课程的id
	}
```

##### GET /api/admin/acceptedCourse
返回course_id 对应的信息

```doc
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
```

##### POST /api/admin/acceptedCourse

修改课程信息

```doc
@param
	id(string):原课程代号
	name(string):课程名称
	hour(read): 课程学时
	credit(real):课程学分
	intro(string):课程介绍
	type(string):课程类型
	exam_date(string): 考试时间
@return
	json object{
		success(bool):操作成功与否
		reason(string):不成功的原因
	}
```






##### GET /api/admin/acceptedTeach
返回已审批teach_id对应的teach信息

```doc
@param
	teach_id(string): teach的id
@return
	json object{
		teach_id(string): 开课id
		tid(string): 老师工号
		capacity(string):课程容量
	}
```


##### POST /api/admin/acceptedTeach
修改已审批teach_id对应的teach信息

```doc
@param
	teach_id(string): teach的id
	tid(string): 老师工号
	capacity(string):课程容量
@return
	json object{
		success(bool):操作成功与否
		reason(string):不成功的原因
	}
```





