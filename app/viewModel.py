from .models import *
from flask import current_app
import json
from sqlalchemy import desc, text
from sqlalchemy.engine.row import Row

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

    def search_staff_by_name(self, name) -> list:
        try:
            results = db.session.execute(
                db.select(
                    Staff.staff_id,
                    Staff.picture_uri,
                    Staff.nrc,
                    Staff.name,
                    Staff.position,   
                    Staff.register_date
            ).where(Staff.name.like(f'%{name}%'))).all()
            
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
        
    def get_guest_info(self, limit: int, offset: int,  order_by_date_desc=True) -> list:
        try:
            query = db.select(
                Guest.guest_id,
                Guest.picture_uri,
                Guest.name,
                Guest.token,   
                Guest.people_count,
                Guest.register_date
            ).limit(limit).offset(offset)
            
            if order_by_date_desc:
                query = query.order_by(desc(Guest.register_date))
            
            results = db.session.execute(query).all()
            guests = [
                {
                    "guest_id": row[0],
                    "picture_uri": row[1],
                    # "nrc": row[2],
                    "name": row[2],
                    "token": row[3],
                    "people_count": row[4],
                    "register_date": str(row[4])
                }
                for row in results
            ]
            return guests
        except Exception as err:
            print(err)
            return []
        
    def search_by_guest_name(self, name) -> list:
        try:
            results = db.session.execute(
                db.select(
                Guest.guest_id,
                Guest.picture_uri,
                Guest.name,
                Guest.token,   
                Guest.register_date
            ).where(Guest.name.like(f'%{name}%'))).all()
            guests = [
                {
                    "guest_id": row[0],
                    "picture_uri": row[1],
                    # "nrc": row[2],
                    "name": row[2],
                    "token": row[3],
                    "register_date": str(row[4])
                }
                for row in results
            ]
            return guests
        except Exception as err:
            print(err)
            return []
    
    def get_passes_by_date(self, date: datetime = None) -> list:
        try:
            from .sort_times import BST
            
            intime = InTime()
            outtime = OutTime()
            times = []
            times += intime.query.all() if not date else db.session.execute(db.select(InTime).where(InTime.time.like(f'%{date}%'))).all()
            times += outtime.query.all() if not date else db.session.execute(db.select(OutTime).where(OutTime.time.like(f'%{date}%'))).all()
            # convert pure object when using db.session.execute return sqlalchemy.engine.row instance
            times = [time[0] if isinstance(time, Row) else time for time in times]
            # for time in times:
            #     print(time)
            tree = BST(times)
            tree.sort()
            times = tree.SORTED_DATA
            time_datas = []
            for time in times:
                time_datas.append(self.__generate_formatted_time_data(time))
            # current_app.logger.info(time_datas)
            return time_datas
        except Exception as err:
            current_app.logger.error(err)
            
        
    def __generate_formatted_time_data(self, time) -> dict:
        try:
            if time:
                time_object = Time.query.get(time.time_id)
                who = self.who_passed(time_object.who_passed)
                p_object = self.__get_object(who[1])
                pass_obj = p_object[2].query.get(time_object.pass_id)
                people_id = self.__get_id_from_object(who[1], pass_obj)
                people = p_object[1].query.get(people_id)
                if people:
                    time_data = {
                        "id": people_id,
                        "profile": people.picture_uri,
                        "name": people.name,
                        "who": who[1],
                        "time": str(time.time.time()),
                        "date": str(time.time.date()),
                        "time_id": time.time_id,
                        "in_out": "IN" if time.in_out else "OUT"
                    }
                    return time_data
            return {}
        except Exception as err:
            current_app.logger.error(err)

            
    def gate_passes(self, which_: str, date: datetime = None) -> list:
        try:
            represent_number, people, people_pass = self.__get_object(which_)
            times = []
            passes = db.session.query(people_pass).order_by(desc(people_pass.date)).all()
            if date:
                passes = db.session.query(people_pass).filter(people_pass.date == date).order_by(desc(people_pass.date)).all()
            for pass_ in passes:
                time = db.session.query(Time).where(Time.who_passed == represent_number, Time.pass_id == pass_.pass_id).first()
                # current_app.logger.info(time.pass_id)
                people_id = self.__get_id_from_object(which_, pass_)
                people = people.query.get(people_id)
                
                people_data = {
                    "name": people.name,
                    "picture_uri": people.picture_uri,
                    f"{which_}_id": people_id,
                    "who": f"{which_}",
                    "time_id": time.id,
                    "is_today": True if datetime.now().date() == time.date else False,
                }
                in_times = []
                for in_time in time.in_passes:
                    in_times.append(str(in_time.time))
                out_times = []
                for out_time in time.out_passes:
                    out_times.append(str(out_time.time))
                in_times = sorted([str(in_time.time) for in_time in time.in_passes], reverse=True)
                out_times = sorted([str(out_time.time) for out_time in time.out_passes], reverse=True)
                data = {
                    "info": people_data,
                    "in_times": in_times,
                    "out_times": out_times
                }
                times.append(data)
            # return sorted([ time for time in times ], reverse=True)
            return times
        except Exception as err:
            current_app.logger.error(err)
            return list()
    
    def get_times(self, time_id: int) -> dict:
        try:
            time = Time.query.get(time_id)
            in_times = time.in_passes
            out_times = time.out_passes
            return {
                "in_times": [str(time.time) for time in in_times],
                "out_times": [str(time.time) for time in out_times]
            }
        except Exception as err:
            current_app.logger.error(err)
            return {
                "in_times": [],
                "out_times": []
            }
    
    def today_pass(self) -> list:
        whos = ["student", "teacher", "staff", "guest"]
        passes = []
        today_pass = []
        for who in whos:
            passes += self.gate_passes(who)
        for pass_ in passes:
            if pass_["info"]["is_today"]:
                today_pass.append(pass_)
        return today_pass
    
    def calculate_today_passed_rate(self) -> list:
        today_pass = self.today_pass()
        student_ = Student.query.all()
        teacher_ = Teacher.query.all()
        staff_ = Staff.query.all()
        guest_ = Guest.query.all()
        
        student = [ people for people in today_pass if people["info"]["who"] == "student" ]
        teacher = [ people for people in today_pass if people["info"]["who"] == "teacher" ]
        staff = [ people for people in today_pass if people["info"]["who"] == "staff" ]
        guest = [ people for people in today_pass if people["info"]["who"] == "guest" ]
        
        rate = {
            "student": "{:.3f}".format((len(student) / len(student_)) * 100),
            "teacher": int((len(teacher) / len(teacher_)) * 100),
            "staff": int((len(staff) / len(staff_)) * 100),
            "guest": int((len(guest) / len(guest_)) * 100) if len(guest_) > 0 else 0
        }
        return rate
    
    def __get_object(self, pronoun: str) -> tuple[object, object]:
        
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
            
    def who_passed(self, number_represent: int) -> str:
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
