from . import db
from datetime import datetime
from sqlalchemy import desc, func

class Admin(db.Model):
    __tablename__ = "admin"
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __str__(self) -> str:
        return self.username

class Student(db.Model):
    __tablename__ = "student"
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    picture_uri = db.Column(db.String(255), nullable=False)
    roll_no = db.Column(db.String(10), nullable=False)
    current_semester = db.Column(db.Integer, nullable=False)
    nrc = db.Column(db.String(100), nullable=False)
    father_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone_no = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(200), nullable=True)
    birth_date = db.Column(db.DateTime, nullable=False)
    register_date = db.Column(db.DateTime, default=datetime.now())
    passes = db.relationship("StudentPass", backref="student", lazy=True, cascade="all, delete")

    def is_new_student(self) -> bool:
        return self.current_semester == 1
    
    def __str__(self) -> str:
        return f"name - {self.name}, roll_no - {self.roll_no}"

class Teacher(db.Model):
    __tablename__ = "teacher"
    teacher_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    picture_uri = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(150), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    nrc = db.Column(db.String(100), nullable=False)
    father_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone_no = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(200), nullable=True)
    birth_date = db.Column(db.DateTime, nullable=False)
    register_date = db.Column(db.DateTime, default=datetime.now().date())
    passes = db.relationship("TeacherPass", backref="teacher", lazy=True, cascade="all, delete")
    
    def __str__(self) -> str:
        return f"<teacher_id: {self.teacher_id}, name: {self.name}>"

class Staff(db.Model):
    __tablename__ = "staff"
    staff_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    picture_uri = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    father_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone_no = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(200), nullable=True)
    nrc = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    register_date = db.Column(db.DateTime, default=datetime.now())
    passes = db.relationship("StaffPass", backref="staff", lazy=True, cascade="all, delete")
    
    def __str__(self) -> str:
        return f"<staff_id: {self.staff_id}, staff_name: {self.name}>"

class Guest(db.Model):
    __tablename__ = "guest"
    guest_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    picture_uri = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    token = db.Column(db.String(200), nullable=False, unique=True)
    register_date = db.Column(db.DateTime, default=datetime.now())
    passes = db.relationship("GuestPass", backref="guest", lazy=True, cascade="all, delete")
    
    def __str__(self) -> str:
        return f"{self.token}"

# Pass Classes: Separated Pass classes for each type of entity
class StudentPass(db.Model):
    __tablename__ = "studentpass" 
    pass_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"))
    date = db.Column(db.Date, nullable=False, default=datetime.now().date())
    # times = db.relationship("Time", backref="studentpass", lazy=True, cascade="all, delete")
    
    def __str__(self) -> str:
        return f"<pass_id: {self.pass_id}, student_id: {self.student_id}>"

class TeacherPass(db.Model):
    __tablename__ = "teacherpass" 
    pass_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.teacher_id"))
    date = db.Column(db.Date, nullable=False, default=datetime.now().date())
    # times = db.relationship("Time", backref="teacherpass", lazy=True, cascade="all, delete")
    
    def __str__(self) -> str:
        return f"<pass_id: {self.pass_id}, teacher_id: {self.teacher_id}>"

class StaffPass(db.Model):
    __tablename__ = "staffpass" 
    pass_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.staff_id"))
    date = db.Column(db.Date, nullable=False, default=datetime.now().date())
    # times = db.relationship("Time", backref="staffpass", lazy=True, cascade="all, delete")
    
    def __str__(self) -> str:
        return f"<pass_id: {self.pass_id}, staff_id: {self.staff_id}>"

class GuestPass(db.Model):
    __tablename__ = "guestpass" 
    pass_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guest_id = db.Column(db.Integer, db.ForeignKey("guest.guest_id"))
    date = db.Column(db.Date, nullable=False, default=datetime.now().date())
    # times = db.relationship("Time", backref="guestpass", lazy=True, cascade="all, delete")
    
    def __str__(self) -> str:
        return f"<pass_id: {self.pass_id}, guest_id: {self.guest_id}>"

# Time and Related Classes: Centralized Time records related to different passes
class Time(db.Model):
    __tablename__ = "time"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, default=datetime.now().date())
    pass_id = db.Column(db.Integer, nullable=False)
    who_passed = db.Column(db.Integer, nullable=False)  # 1: student, 2: teacher, 3: staff, 4: guest
    # passes = db.relationship(f"{parent}", backref="time", lazy=True, cascade="all, delete")
    in_passes =  db.relationship("InTime", backref="related_time", lazy=True, cascade="all, delete")
    out_passes = db.relationship("OutTime", backref="related_time", lazy=True, cascade="all, delete")
    
    def __str__(self) -> str:
        return f"<date - {self.date} >"

class InTime(db.Model):
    __tablename__ = "intime"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, nullable=False)
    time_id = db.Column(db.Integer, db.ForeignKey("time.id"), nullable=False)
    
    def __str__(self):
        return f"<time_id - {self.time_id} >" 
    
class OutTime(db.Model):
    __tablename__ = "outtime"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, nullable=False)    
    time_id = db.Column(db.Integer, db.ForeignKey("time.id"), nullable=False)
    
    def __str__(self):
        return f"<time_id - {self.time_id} >" 


        
