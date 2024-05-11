from . import db
from datetime import datetime, timedelta

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
    register_date = db.Column(db.DateTime, default=datetime.now())

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
    register_date = db.Column(db.DateTime, default=datetime.now())

    def __str__(self) -> str:
        return f"<teacher_id: {self.teacher_id}, name: {self.name}"
    
# class Contact(db.Model):
#     __tablename__ = "contact"

#     contact_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     phone_no = db.Column

def get_student_info() -> list:
    try:
        students = db.session.execute(
                db.select(
                    Student.student_id,
                    Student.name,
                    Student.roll_no,
                    Student.current_semester,   
                    Student.register_date
                )).all()
        return students
    except Exception as err:
        print(err)
        return list()