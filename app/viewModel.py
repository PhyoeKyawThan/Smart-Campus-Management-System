from .models import *
from flask import current_app

class ViewModel():
    def __init__(self) -> None:
        pass
    
    def get_student_info(self) -> list:
        try:
            students = db.session.execute(
                db.select(
                    Student.student_id,
                    Student.picture_uri,
                    Student.name,
                    Student.roll_no,
                    Student.current_semester,   
                    Student.register_date
                )
            ).all()
            return students
        except Exception as err:
            print(err)
            return list()
    
    def get_teacher_info(self) -> list:
        try:
            teachers = db.session.execute(
                db.select(
                    Teacher.teacher_id,
                    Teacher.picture_uri,
                    Teacher.name,
                    Teacher.department,
                    Teacher.position,   
                    Teacher.register_date
                )
            ).all()
            return teachers
        except Exception as err:
            return list()
    
    def get_staff_info(self) -> list:
        try:
            staffs = db.session.execute(
                db.select(
                    Staff.staff_id,
                    Staff.picture_uri,
                    Staff.nrc,
                    Staff.name,
                    Staff.position,   
                    Staff.register_date
                )
            ).all()
            return staffs
        except Exception as err:
            return list()

    def get_guest_info(self) -> list:
        try:
            guests = db.session.execute(
                db.select(
                    Guest.guest_id,
                    Guest.picture_uri,
                    Guest.name,
                    Guest.token,   
                    Guest.register_date
                )
            ).all()
            return guests
        except Exception as err:
            return list()
    
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
