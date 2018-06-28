from django.db import models
from basicInfo.config import course_type

class observer:
    def __init__(self):
        pass
    def update(self,*text):
        pass

class OperationObserver(observer):
    def update(self,*text):
        operation.objects.create(description=text[0])
        print("log saved")

class TeacherObserver(observer):
    def update(self,*text):
        teacher.objects.create(*text)


class account(models.Model):
    '''
    accout(accout_id int, password varchar(20) not null) //统一账户
    '''

    observers=[OperationObserver(),TeacherObserver()]  # observer list
    account_id=models.CharField(max_length=20,primary_key=True)
    password=models.CharField(max_length=200,null=False)
    salt=models.CharField(max_length=8,null=False,default="12345678")
    type=models.IntegerField(null=False,default=0)

    def save(self, *args, **kwargs):
        print("account saved")
        super(account, self).save(*args, **kwargs)


class attrib(models.Model):
    '''
    attrib(account_id int, nickname varchar(40), picture varchar(40)), email varchar(40), exp int, coin int) //账户属性 ref account
    '''

    account_id=models.ForeignKey(account,on_delete=models.CASCADE,primary_key=True)
    nickname=models.CharField(max_length=40,null=False)
    picture=models.ImageField(upload_to="basicInfo/static/basicInfo/picture",null=True)
    email=models.CharField(max_length=40,null=True)
    exp=models.IntegerField(null=True)
    coin=models.IntegerField(null=True)


class student(models.Model):
    '''
    student(student_id int, name varchar(20) not null, dorm varchar(40)) //学生
    '''

    student_id=models.CharField(max_length=20,primary_key=True)
    name=models.CharField(max_length=20,null=False)
    dorm=models.CharField(max_length=40)
    grade=models.IntegerField(default=1)


class college(models.Model):
    '''
    college(college_id int, name varchar(40) not null, intro text) //学院
    '''

    college_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=40,null=False)
    intro=models.TextField()


class discipline(models.Model):
    '''
    discipline(discipline_id int, name varchar(40) not null, intro text) //专业
    '''

    discipline_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=40,null=False)
    intro=models.TextField()


class major(models.Model):
    '''
    major(student_id int, discipline_id int) //主修 ref student, discipline
    '''

    student_id=models.CharField(max_length=20,primary_key=True)
    discipline_id=models.IntegerField()
    class Meta:
        unique_together = ("student_id", "discipline_id")
    primary = ("student_id", "discipline_id")


class minor(models.Model):
    '''
    minor(student_id int, discipline_id int) //辅修 ref student, discipline
    '''

    student_id=models.CharField(max_length=20,primary_key=True)
    discipline_id = models.IntegerField()
    class Meta:
        unique_together = ("student_id", "discipline_id")
    primary = ("student_id", "discipline_id")


class belong(models.Model):
    '''
    belong(major_id int, college_id int) //专业所在学院 ref major, college
    '''

    discipline_id=models.ForeignKey(discipline,on_delete=models.CASCADE)
    college_id=models.ForeignKey(college,on_delete=models.CASCADE)
    class Meta:
        unique_together = ("discipline_id", "college_id")
    primary=("discipline_id", "college_id")


class course(models.Model):
    '''
    course(course_id int, name varchar(40) not null, credit real not null, capacity int not null, intro text, type varchar(40) not null) //课程
    '''

    course_id=models.CharField(max_length=10,primary_key=True)
    name=models.CharField(max_length=40,null=False)
    credit=models.DecimalField(max_digits=3,decimal_places=1)
    hour=models.FloatField()
    intro=models.TextField()
    duplicate = models.IntegerField(default=0)
    type=models.CharField(max_length=40,null=False,choices=course_type,default="0")
    semester=models.CharField(max_length=10,null=False,default="Spring")
    exam_date = models.DateTimeField(null=True)

class pre(models.Model):
    '''
    pre(tmp_course_id int, pre_course_id int) //课程预修 ref course
    '''
    tmp_course_id=models.IntegerField()
    pre_course_id=models.ForeignKey(course,on_delete=models.CASCADE)
    class Meta:
        unique_together=("tmp_course_id","pre_course_id")
    primary = ("tmp_course_id","pre_course_id")


class room(models.Model):
    '''
    room(room_id int, capacity int not null, location varchar(40) not null, type varchar(40) not null) //教室
    '''
    room_id=models.AutoField(primary_key=True)
    capacity=models.IntegerField(null=False)
    location=models.CharField(max_length=40,null=False)
    type=models.CharField(max_length=40,null=False)


class learn(models.Model):
    '''
    learn(student_id int, course_id int, grade int, status int) //参加课程 ref student, course
    '''

    student_id=models.ForeignKey(student,on_delete=models.CASCADE)
    course_id=models.ForeignKey(course,on_delete=models.CASCADE)
    grade=models.IntegerField(null=True)
    status=models.IntegerField(null=False,default=0)
    class Meta:
        unique_together=("student_id","course_id")
    primary=("student_id","course_id")


class time(models.Model):
    '''
    time(time_id int ,start time not null, end time not null, day int not null) // 时间段 const
    '''

    time_id=models.AutoField(primary_key=True)
    start=models.TimeField(null=False)
    end=models.TimeField(null=False)
    day=models.IntegerField(null=False)


class teacher(models.Model):
    '''
    teacher(teacher_id int, name varchar(20) not null) //教师
    '''

    teacher_id=models.ForeignKey(account,on_delete=models.CASCADE,related_name="teacherId",primary_key=True)
    name=models.CharField(max_length=20,null=False)
    title=models.CharField(max_length=10,null=False,default="lecturer")
    office=models.CharField(max_length=40,null=False)
    management=models.CharField(max_length=40,null=True)


class teach(models.Model):
    '''
    teach(teacher_id int, course_id int) //讲授课程 ref teacher, course
    '''

    teach_id=models.AutoField(primary_key=True)
    teacher_id=models.ForeignKey(teacher,on_delete=models.CASCADE,related_name="teacher_id_1")
    course_id=models.ForeignKey(course,on_delete=models.CASCADE,related_name="college_id_1")
    capacity=models.IntegerField(null=False)


class readyteach(models.Model):
    '''
    readyteach(teacher_id int, course_id int) //讲授课程 ref teacher, course
    '''

    teacher_id=models.ForeignKey(teacher,on_delete=models.CASCADE)
    course_id=models.ForeignKey(course,on_delete=models.CASCADE)
    capacity=models.IntegerField(null=False)


class takeup(models.Model):
    '''
    takeup(course_id int, time_id int, room_id int, type int not null) //课程时空信息 ref course, time, room
    '''

    teach_id=models.ForeignKey(teach,on_delete=models.CASCADE)
    time_id=models.ForeignKey(time,on_delete=models.CASCADE)
    room_id=models.ForeignKey(room,on_delete=models.CASCADE)
    teacher_id=models.ForeignKey(teacher,on_delete=models.CASCADE)
    class Meta:
        unique_together = ("teach_id", "time_id","room_id")
    primary = ("teach_id", "time_id","room_id")


class examination(models.Model):
    '''
    exam(student_id int, takeup_id int, position int)//考生座位信息 ref student, takeup
    '''

    student_id=models.ForeignKey(student,on_delete=models.CASCADE)
    takeup_id=models.ForeignKey(takeup,on_delete=models.CASCADE)
    position=models.IntegerField(null=True)
    class Meta:
        unique_together = ("student_id", "takeup_id","position")
    primary = ("student_id", "takeup_id","position")


class evaluate(models.Model):
    '''
    evalueate(student_id int, teacher_id int, point real not null, description text) //学生评价 ref student, teacher
    '''
    student_id=models.ForeignKey(student,on_delete=models.CASCADE)
    teacher_id=models.ForeignKey(teacher,on_delete=models.CASCADE)
    point=models.DecimalField(max_digits=3,decimal_places=2)
    description=models.TextField()
    class Meta:
        unique_together = ("student_id", "teacher_id")
    primary = ("student_id", "teacher_id")


class work(models.Model):
    '''
    work(teacher_id int, college_id int) //归属学院 ref teacher, college
    '''

    teacher_id=models.ForeignKey(teacher,on_delete=models.CASCADE)
    college_id=models.ForeignKey(college,on_delete=models.CASCADE)
    class Meta:
        unique_together = ("teacher_id","college_id")
    primary = ("teacher_id","college_id")


class master(models.Model):
    '''
    master(teacher_id int, college_id int) //管理学院 ref teacher, college
    '''
    teacher_id=models.ForeignKey(teacher,on_delete=models.CASCADE)
    college_id=models.ForeignKey(college,on_delete=models.CASCADE)
    class Meta:
        unique_together = ("teacher_id","college_id")
    primary = ("teacher_id","college_id")


class assist(models.Model):
    '''
    assist(student_id int, course_id int) //助教 ref student, course
    '''

    student_id = models.ForeignKey(student, on_delete=models.CASCADE)
    course_id = models.ForeignKey(course, on_delete=models.CASCADE)
    class Meta:
        unique_together = ("student_id", "course_id")
    primary = ("student_id", "course_id")


class admin(models.Model):
    '''
    admin(admin_id int, name varchar(20) not null) //系统管理员
    '''
    admin_id=models.CharField(max_length=20,primary_key=True)
    name=models.CharField(max_length=20,null=False)


class operation(models.Model):
    '''
    operation(operation_id int, description text not null) //表操作 const
    '''
    operation_id=models.AutoField(primary_key=True)
    description=models.TextField(null=False)


class log(models.Model):
    '''
    log(log_id int, operation_id int, time time not null, content text) //操作记录 ref operation
    '''
    log_id=models.AutoField(primary_key=True)
    operation_id=models.ForeignKey(operation,on_delete=models.CASCADE)
    time=models.DateTimeField(auto_now_add=True,null=False)
    content=models.TextField()
