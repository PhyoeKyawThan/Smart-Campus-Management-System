from datetime import datetime 
from ..models import *
from werkzeug.security import check_password_hash
from flask import current_app
import json

class Track:
    def __init__(self, who: str) -> None:
        self.who: str = who
    
    def __check_is_today(self, exist_date: datetime) -> bool:
        """
        check where the incoming pass is today or not
        for reduce exception between trackpass and time
        """        
        current = datetime.now().date()
        current_date = datetime(current.year, current.month, current.day)
        try:
            time = Time.query.filter_by(date=exist_date).first()
            if time:
                if( current_date == exist_date ):
                    return True
        except Exception as e:
            current_app.logger.error(e)
            return False    
    
    def __get_object(self) -> tuple:
        match self.who:
            case "student":
                return ( Student, StudentPass )
            case "teacher":
                return ( Teacher, TeacherPass )
            case "staff":
                return ( Staff, StaffPass )
            case "guest":
                return ( Guest, GuestPass )
            case _:
                return None
        
    
    def __set_id_to_pass(self, pass_obj: Time, id: int)->None:
        match self.who:
            case "student":
                pass_obj.student_id = id
            case "teacher":
                pass_obj.teacher_id = id
            case "staff":
                pass_obj.staff_id = id
            case "guest":
                pass_obj.guest_id = id
            case _:
                return None
    
    def __get_id_from_object(self, people: object) -> int:
        match self.who:
            case "student":
                return people.student_id
            case "teacher":
                return people.teacher_id
            case "staff":
                return people.staff_id
            case "guest":
                return people.guest_id
            case _:
                return None
    def __passed_today(self, id: int) -> object:
        """
        get id as args and check is already today passed 
        return exist trackpass object or new trackpass
        """
        try:
            track_pass = TrackPass.query.filter_by(**{
            f"{self.who}_id": id,
            "date": datetime.now().date()
            }).first()
            if track_pass:
                return track_pass
        except Exception as e:
            current_app.logger.error(e)
        return TrackPass()
    
    def __check(self, unique_id: str, token: str)->bool:
        try:
            people = self.__get_object().query.filter_by(**{f"{self.who}_id": unique_id}).first()
            if people:
                formatted_data = self.__get_format(people=people)
                if check_password_hash(token, json.dumps(formatted_data)):
                    # add logging for test
                    current_app.logger.info(f"username = {people.name} is validate")
                    today_passed_people =self.__passed_today(unique_id)
                    if self.__get_id_from_object(today_passed_people):
                        if (len(today_passed_people.times) + 1) % 2 != 0:
                            in_time = Time()
                            in_time.in_time = datetime.now()
                            in_time.pass_id = today_passed_people.pass_id
                            db.session.add(in_time)
                            db.session.commit()
                            return True
                        out_time = Time()
                        out_time.out_time = datetime.now()
                        out_time.pass_id = today_passed_people.pass_id
                        db.session.add(out_time)
                        db.session.commit()
                        return True
                    # create new in coming pass
                    new_in_pass_people = TrackPass()
                    self.__set_id_to_pass(new_in_pass_people, self.__get_id_from_object(people=people))
                    db.session.add(new_in_pass_people)
                    db.session.commit()
                    # create new in time data 
                    new_in_pass_time = Time()
                    new_in_pass_time.in_time = datetime.now()
                    new_in_pass_time.pass_id = new_in_pass_people.pass_id
                    db.session.add(new_in_pass_time)
                    db.session.commit()
                    return True
        except Exception as e:
            current_app.logger.error(e)
            return False
        
    def add_pass(self, datas: dict) -> bool:
        if self.__check(datas["id"], datas["token"]):
            return True
        return False
    
    
    def __get_format(self, people: object)->dict:
        match self.who:
            case "student":
                return {
                    "student_id": people.student_id,
                    "name": people.name,
                    "roll_no": people.roll_no,
                    "father_name": people.father_name,
                    "current_semester": people.current_semester
                }
            case "teacher":
                return {
                    "teacher_id": people.teacher_id,
                    "name": people.name,
                    "department": people.department,
                    "position": people.position,
                    "nrc": people.nrc,
                    "birth_date": str(people.birth_date)
                }
            case "staff":
                return {
                    "staff_id": people.staff_id,
                    "name": people.name,
                    "position": people.position,
                    "birth_date": str(people.birth_date)
                }
            case "guest":
                return {
                    "guest_id": people.guest_id,
                    "name": people.name,
                    "token": people.token,
                    "register_date": people.register_date
                }
                
            case _:
                return None
    def __str__(self) -> str:
        return f"< who_pass = {self.who} >"