from .models import Student, Admin
from flask import session

def student_exists(name: str, roll_no: str)->bool:
    """
    parems: name, roll_no
    summery: check the student is already exists or not by name and roll_no and return boolean result
    """
    student = Student.query.filter_by(name=name, roll_no=roll_no).first()
    if student:
        return True
    return False

def is_admin(username: str, password: str)->bool:
    """
    parems: username: from form data, password: from form data
    summery: check admin is admin or not by username and password provided by client admin
    """
    admin = Admin.query.filter_by(username=username, password=password).first()
    if admin:
        return True
    return False


def check_admin_in_session()->bool:
    try:
        if "current_admin" in session:
            try:
                admin = session["current_admin"]
                admin = Admin.query.filter_by(username=admin["username"], password=admin["password"]).first()
                print(admin)
                if admin:
                    return True
                return False
            except KeyError as err:
                print(err)
                return False
    except Exception as err:
        print(err)
        return False