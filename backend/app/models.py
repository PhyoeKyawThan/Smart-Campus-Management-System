from . import db
from datetime import datetime, timedelta, date
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
    track_passes = db.relationship("TrackPass", backref="student", lazy=True, cascade="all, delete")

    def is_new_student(self) -> bool:
        """
        summery: this function will check student is new or not by their current_semester
        return_type: boolean
        """
        return True if self.current_semester == 1 else False
    
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
    track_passes = db.relationship("TrackPass", backref="teacher", lazy=True, cascade="all, delete")
    
    def __str__(self) -> str:
        return f"<teacher_id: {self.teacher_id}, name: {self.name}"

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
    register_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    track_passes = db.relationship("TrackPass", backref="staff", lazy=True, cascade="all, delete")
    
    def __str__(self) -> str:
        return f"< staff_id: {self.staff_id}, staff_name: {self.name} >"

class Guest(db.Model):
    __tablename__ = "guest"
    
    guest_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    picture_uri = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    token = db.Column(db.String(200), nullable=False, unique=True)
    register_date = db.Column(db.DateTime, default=datetime.now())
    track_passes = db.relationship("TrackPass", backref="guest", lazy=True, cascade="all, delete")
    
    def __str__(self) -> str:
        return f"{self.token}"
    
class TrackPass(db.Model):
    __tablename__ = "trackpass"
    
    pass_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"))
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.teacher_id"))
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.staff_id"))
    guest_id = db.Column(db.Integer, db.ForeignKey("guest.guest_id"))
    date = db.Column(db.Date, nullable=True, default=datetime.now().date())
    times = db.relationship("Time", backref="trackpass", lazy=True, cascade="all, delete")
    
    
    def __str__(self) -> str:
        if self.student_id:
            return f"< student_id: {self.student_id}, pass_id: {self.pass_id} >"
        if self.teacher_id:
            return f"< teacher_id: {self.teacher_id}, pass_id: {self.pass_id} >"
        return "<>"

class Time(db.Model):
    __tablename__ = "time"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, default=datetime.now().date())
    in_time = db.Column(db.DateTime, nullable=True)
    out_time = db.Column(db.DateTime, nullable=True)
    pass_id = db.Column(db.Integer, db.ForeignKey("trackpass.pass_id"), nullable=False)
    
    def __str__(self) -> str:
        return f"In - {self.in_time} -> Out - {self.out_time}"

def get_student_info() -> list:
    """
    get all student data( student_id,
    name, roll_no, current_semester, register_date )
    """
    try:
        students = db.session.execute(
                db.select(
                    Student.student_id,
                    Student.picture_uri,
                    Student.name,
                    Student.roll_no,
                    Student.current_semester,   
                    Student.register_date
                )).all()
        return students
    except Exception as err:
        print(err)
        return list()

def get_teacher_info() -> list:
    """
    get all teacher data( teacher_id,
    name, department, position, register_date )
    """
    try:
        teachers = db.session.execute(
                db.select(
                    Teacher.teacher_id,
                    Teacher.picture_uri,
                    Teacher.name,
                    Teacher.department,
                    Teacher.position,   
                    Teacher.register_date
                )).all()
        return teachers
    except Exception as err:
        return list()
    
def get_staff_info() -> list:
    """
    get all staff data( staff_id, picture_uri,
    name,  position, register_date )
    """
    try:
        staffs = db.session.execute(
                db.select(
                    Staff.staff_id,
                    Staff.picture_uri,
                    Staff.name,
                    Staff.position,   
                    Staff.register_date
                )).all()
        return staffs
    except Exception as err:
        return list()

def get_guest_info() -> list:
    """
    get all guest data( guest_id, picture_uri,
    name,  position, register_date )
    """
    try:
        guest = db.session.execute(
                db.select(
                    Guest.guest_id,
                    Guest.picture_uri,
                    Guest.name,
                    Guest.token,   
                    Guest.register_date
                )).all()
        return guest
    except Exception as err:
        return list()

def get_trackpass() -> list:
    try:
        # Assuming `session` is your SQLAlchemy session
        passes_student = db.session.query(
            Student.student_id, 
            Student.picture_uri, 
            Student.name, 
            TrackPass.in_time, 
            TrackPass.out_time,
            TrackPass.pass_id
        ).join(TrackPass, 
               Student.student_id == TrackPass.student_id).order_by(desc(TrackPass.pass_id)).all()
        passes_teacher = db.session.query(
            Teacher.teacher_id, 
            Teacher.picture_uri, 
            Teacher.name, 
            TrackPass.in_time, 
            TrackPass.out_time,
            TrackPass.pass_id
        ).join(TrackPass, 
               Teacher.teacher_id == TrackPass.teacher_id).order_by(desc(TrackPass.pass_id)).all()
        passes_guest = db.session.query(
            Guest.guest_id, 
            Guest.picture_uri, 
            Guest.name, 
            TrackPass.in_time, 
            TrackPass.out_time,
            TrackPass.pass_id
        ).join(TrackPass, 
               Guest.guest_id == TrackPass.guest_id).order_by(desc(TrackPass.pass_id)).all()
        passess_staff = db.session.query(
            Staff.staff_id, 
            Staff.picture_uri, 
            Staff.name, 
            TrackPass.in_time, 
            TrackPass.out_time,
            TrackPass.pass_id
        ).join(TrackPass, 
               Staff.staff_id == TrackPass.staff_id).order_by(desc(TrackPass.pass_id)).all()
        passess = passes_student + passes_guest + passes_teacher + passess_staff
        all_passes_sorted = sorted(passess, key=lambda x: x.pass_id, reverse=True)
        return all_passes_sorted
    
    except Exception as err:
        # Log the error
        print(f"An error occurred: {err}")
        return []


def recent_pass() -> list:
    try:
        # Assuming `session` is your SQLAlchemy session
        today = datetime.now().date()
        recent_passes = db.session.query(
            Student.student_id, 
            Student.picture_uri, 
            Student.name, 
            TrackPass.in_time, 
            TrackPass.out_time,
            TrackPass.pass_id
        ).join(TrackPass, 
               Student.student_id == TrackPass.student_id).filter( func.date(TrackPass.in_time) == today ).order_by(desc(TrackPass.pass_id)).all()
        return recent_passes[:5]
    except Exception as err:
        # Log the error
        print(f"An error occurred: {err}")
        return []