from .models import *
from flask import current_app
from sqlalchemy import desc

class ViewModel():
    def __init__(self) -> None:
        pass
    
    def get_student_info(self, limit=10, offset=0, order_by_date_desc=True) -> list:
        try:
            query = db.select(
                Student.student_id,
                Student.picture_uri,
                Student.name,
                Student.roll_no,
                Student.current_semester,   
                Student.register_date
            ).limit(limit).offset(offset)
            
            if order_by_date_desc:
                query = query.order_by(desc(Student.register_date))
            
            results = db.session.execute(query).all()
            
            students = [
                {
                    "student_id": row[0],
                    "picture_uri": row[1],
                    "name": row[2],
                    "roll_no": row[3],
                    "current_semester": row[4],
                    "register_date": str(row[5])
                }
                for row in results
            ]
            return students
        except Exception as err:
            print(err)
            return []
        
    def search_student_by_roll(self, roll_no) -> list:
        try:
            # Adjust the query to use `like()` for searching roll_no
            results = db.session.execute(
                db.select(
                    Student.student_id,
                    Student.picture_uri,
                    Student.name,
                    Student.roll_no,
                    Student.current_semester,
                    Student.register_date
                ).where(Student.roll_no.like(f'%{roll_no}%'))  # Using LIKE for partial matching
            ).all()
            students = [
                {
                    "student_id": row[0],
                    "picture_uri": row[1],
                    "name": row[2],
                    "roll_no": row[3],
                    "current_semester": row[4],
                    "register_date": str(row[5])
                }
                for row in results
                
            ]
            return students
        except Exception as err:
            print(err)
            return []

    
    def get_teacher_info(self, limit=10, offset=0, order_by_date_desc=True) -> list:
        try:
            query = db.select(
                Teacher.teacher_id,
                Teacher.picture_uri,
                Teacher.name,
                Teacher.department,
                Teacher.position,   
                Teacher.register_date
            ).limit(limit).offset(offset)
            
            if order_by_date_desc:
                query = query.order_by(desc(Teacher.register_date))
            
            results = db.session.execute(query).all()
            teachers = [
                {
                    "teacher_id": row[0],
                    "picture_uri": row[1],
                    "name": row[2],
                    "department": row[3],
                    "position": row[4],
                    "register_date": str(row[5])
                }
                for row in results
                
            ]
            return teachers
        except Exception as err:
            print(err)
            return []
    
    def search_teacher_by_name(self, name) -> list:
        try:
            # Adjust the query to use `like()` for searching roll_no
            results = db.session.execute(
                db.select(
                    Teacher.teacher_id,
                    Teacher.picture_uri,
                    Teacher.name,
                    Teacher.department,
                    Teacher.position,   
                    Teacher.register_date
                ).where(Teacher.name.like(f'%{name}%'))  # Using LIKE for partial matching
            ).all()
            teachers = [
                {
                    "teacher_id": row[0],
                    "picture_uri": row[1],
                    "name": row[2],
                    "department": row[3],
                    "position": row[4],
                    "register_date": str(row[5])
                }
                for row in results
                
            ]
            return teachers
        except Exception as err:
            print(err)
            return []
    
    def get_staff_info(self, limit=10, offset=0, order_by_date_desc=True) -> list:
        try:
            query = db.select(
                Staff.staff_id,
                Staff.picture_uri,
                Staff.nrc,
                Staff.name,
                Staff.position,   
                Staff.register_date
            ).limit(limit).offset(offset)
            
            if order_by_date_desc:
                query = query.order_by(desc(Staff.register_date))
            
            results = db.session.execute(query).all()
            staffs = [
                {
                    "staff_id": row[0],
                    "picture_uri": row[1],
                    "nrc": row[2],
                    "name": row[3],
                    "position": row[4],
                    "register_date": str(row[5])
                }
                for row in results
            ]
            return staffs
        except Exception as err:
            print(err)
            return []


    def get_guest_info(self, order_by_date_desc=True) -> list:
        try:
            query = db.select(
                Guest.guest_id,
                Guest.picture_uri,
                Guest.name,
                Guest.token,   
                Guest.register_date
            )
            
            if order_by_date_desc:
                query = query.order_by(desc(Guest.register_date))
            
            guests = db.session.execute(query).all()
            return guests
        except Exception as err:
            print(err)
            return []
    
    def gate_passes(self, which_: str) -> list:
        try:
            represent_number, people, people_pass = self.__get_object(which_)
            times = []
            passes = db.session.query(people_pass).order_by(desc(people_pass.date)).all()
            for pass_ in passes:
                time = db.session.query(Time).where(Time.who_passed == represent_number, Time.pass_id == pass_.pass_id).first()
                current_app.logger.info(time.pass_id)
                people_id = self.__get_id_from_object(which_, pass_)
                people = people.query.get(people_id)
                current_app.logger.info(people)
                people_data = {
                    "name": people.name,
                    "picture_uri": people.picture_uri,
                    f"{which_}_id": people_id,
                    "is_today": True if datetime.now().date() == time.date else False,
                }
                in_times = []
                for in_time in time.in_passes:
                    in_times.append(str(in_time.time))
                out_times = []
                for out_time in time.out_passes:
                    out_times.append(str(out_time.time))
                data = {
                    "info": people_data,
                    "in_times": in_times,
                    "out_times": out_times
                }
                times.append(data)
                print(data)
            return times
        except Exception as err:
            current_app.logger.error(err)
            return list()
    
    
    
    def __get_object(self, pronoun: int) -> tuple[object, object]:
        
        match pronoun:
            case "student":
                return  1, Student, StudentPass 
            
            case "teacher":
                return  2, Teacher, TeacherPass 
            
            case "staff":
                return  3, Staff, StaffPass 
            
            case "guest":
                return  4, Guest, GuestPass 
            
            case _:
                return None, None
            
    def who_passed(number_represent: int) -> str:
        match number_represent:
            case 1:
                return 1, "student"
            
            case 2:
                return 2, "teacher"
            
            case 3:
                return 3, "staff"
            
            case 4:
                return 4, "guest"
            
            case _:
                return 0

    def __get_id_from_object(self, which_: str, object: object) -> int:
        
        match which_:
            case "student":
                return object.student_id
            case "teacher":
                return object.teacher_id
            case "staff":
                return object.staff_id
            case "guest":
                return object.guest_id
            case _:
                return None
