from datetime import datetime 
from ..models import *

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
        time = Time.query.filter_by(date=exist_date).first()
        if time:
            if( current_date == exist_date ):
                return True
        return False    
    
    def __get_object(self):
        match self.who:
            case "student":
                return Student
            case "teacher":
                return Teacher
            case "staff":
                return Staff
            case "guest":
                return Guest
            case _:
                raise None
    
    def __passed_today(self, id: int) -> TrackPass:
        """
        get id as args and check is already today passed 
        return exist trackpass object or new trackpass
        """
        track_pass = TrackPass.query.filter_by(**{
            f"{self.who}_id": id,
            "date": datetime.now().date()
            }).first()
        if track_pass:
            return track_pass
        return TrackPass()
    
    def __check(self, unique_id: str)->bool:
        people = self.__get_object().query.filter_by(**{f"{self.who}_id": unique_id}).first()
        if people:
            pass
        
    def add_pass(self, datas: dict) -> bool:
        pass
    
    
    def __get_format(self, datas: list)->dict:
        match self.who:
            case "student":
                return {
                    "student_id": datas[0],
                    "name": datas[1],
                    "roll_no": datas[2],
                    "father_name": datas[3],
                    "current_semester": datas[4] 
                }
            case "teacher":
                return {
                    "teacher_id": datas[0],
                    "name": datas[1],
                    "department": datas[2],
                    "position": datas[3],
                    "nrc": datas[4],
                    "birth_date": datas[5]
                }
            case "staff":
                return {
                    "staff_id": datas[0],
                    "name": datas[1],
                    "position": datas[2],
                    "birth_date": datas[3]
                }
            case "guest":
                return {
                    "guest_id": datas[0],
                    "name": datas[1],
                    "token": datas[2],
                    "register_date": datas[3]
                }
                
            case _:
                return None