from datetime import datetime
from ..models import * 
from werkzeug.security import check_password_hash
from flask import current_app
import json

class Track:
    """
    Track class to handle pass management for different types of users (student, teacher, staff, guest).

    Attributes:
        who (str): The type of user (student, teacher, staff, guest).
    """

    def __init__(self, who: str) -> None:
        """
        Initializes the Track class with the user type.

        Args:
            who (str): The type of user (student, teacher, staff, guest).
        """
        self.who = who

    def __get_object(self) -> tuple:
        """
        Returns the appropriate model and pass model based on the user type.

        Returns:
            tuple: A tuple containing the user model and the pass model.
        """
        match self.who:
            case "student":
                return (Student, StudentPass)
            case "teacher":
                return (Teacher, TeacherPass)
            case "staff":
                return (Staff, StaffPass)
            case "guest":
                return (Guest, GuestPass)
            case _:
                return None

    def __get_id_from_object(self, people: object) -> int:
        """
        Retrieves the ID from the user object based on the user type.

        Args:
            people (object): The user object.

        Returns:
            int: The user ID.
        """
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

    def __get_int_represent(self) -> int:
        """
        Returns an integer representation for the user type.

        Returns:
            int: Integer representing the user type (1 for student, 2 for teacher, 3 for staff, 4 for guest).
        """
        match self.who:
            case "student":
                return 1
            case "teacher":
                return 2
            case "staff":
                return 3
            case "guest":
                return 4
            case _:
                return 0

    def __set_id_to_pass(self, pass_object: object, id: int) -> None:
        """
        Sets the user ID to the pass object.

        Args:
            pass_object (object): The pass object.
            id (int): The user ID.
        """
        setattr(pass_object, f"{self.who}_id", id)

    def __passed_today(self, id: int) -> object:
        """
        Checks if the user has already passed today.

        Args:
            id (int): The user ID.

        Returns:
            object: The pass object if the user has passed today, None otherwise.
        """
        try:
            target_object = self.__get_object()[1]()
            pass_object = target_object.query.filter_by(**{
                f"{self.who}_id": id,
                "date": datetime.now().date()
            }).first()
            if pass_object:
                return pass_object
        except Exception as e:
            current_app.logger.error(e)
            return None
        return target_object

    def __check(self, unique_id: int, token: str) -> bool:
        """
        Validates the user's token and handles the pass entry/exit logic.

        Args:
            unique_id (int): The user ID.
            token (str): The token to validate.

        Returns:
            bool: True if the token is valid and the pass is successfully added/updated, False otherwise.
        """
        try:
            target_object = self.__get_object()[0]
            people = target_object.query.filter_by(**{
                f"{self.who}_id": unique_id
            }).first()
            if people:
                formatted_data = self.__get_format(people=people)
                if check_password_hash(token, json.dumps(formatted_data)):
                    current_app.logger.info(f"username = {people.name} is valid")
                    today_passed_people = self.__passed_today(unique_id)
                    if self.__get_id_from_object(today_passed_people):
                        time = Time.query.filter_by(pass_id=today_passed_people.pass_id).first()
                        total_pass = len(time.in_passes) + len(time.out_passes)
                        if ((total_pass + 1) % 2) != 0:
                            in_time = InTime()
                            in_time.time_id = time.id
                            in_time.time = datetime.now()
                            db.session.add(in_time)
                            db.session.commit()
                            return True

                        out_time = OutTime()
                        out_time.time = datetime.now()
                        out_time.time_id = time.id
                        db.session.add(out_time)
                        db.session.commit()
                        return True

                    new_pass = self.__get_object()[1]()
                    self.__set_id_to_pass(new_pass, self.__get_id_from_object(people=people))
                    db.session.add(new_pass)
                    db.session.commit()

                    new_time = Time()
                    new_time.pass_id = new_pass.pass_id
                    new_time.who_passed = self.__get_int_represent()
                    new_time.date = datetime.now()
                    db.session.add(new_time)
                    db.session.commit()

                    new_in_time = InTime()
                    new_in_time.time = datetime.now()
                    new_in_time.time_id = new_time.id
                    db.session.add(new_in_time)
                    db.session.commit()

                    return True

        except Exception as e:
            current_app.logger.error(e)
            return False

    def add_pass(self, datas: dict) -> bool:
        """
        Adds a pass for the user if the token is valid.

        Args:
            datas (dict): A dictionary containing the user ID and token.

        Returns:
            bool: True if the pass is successfully added, False otherwise.
        """
        if self.__check(datas["id"], datas["token"]):
            return True
        return False

    def __get_format(self, people: object) -> dict:
        """
        Formats the user data into a dictionary based on the user type.

        Args:
            people (object): The user object.

        Returns:
            dict: A dictionary containing the formatted user data.
        """
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
