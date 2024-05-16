from ..models import Student, Admin, Teacher, Stuff
from flask import session

def student_exists(roll_no: str)->bool:
    """
    params: roll_no
    summery: check the student is already exists or not by name and roll_no and return boolean result
    """
    try:
        student = Student.query.filter_by(roll_no=roll_no).first()
        if student:
            return True
        return False
    except Exception as err:
        print(err)
        return False

def stuff_exists(name: str, position: str) -> bool:
    """
    params: name: str, position: str
    summery: check the stuff is already exist or not when register new stuff
    """
    try:
        stuff = Stuff.query.filter_by(name=name, position=position).first()
        if stuff:
            return True
        return False
    except Exception as err:
        print(err)
        return False

def teacher_exists(name: str, department: str, position: str) -> bool:
    teacher = Teacher.query.filter_by(name=name,
                                      department=department,
                                      position=position).first()
    if teacher:
        return True
    return False

def is_admin(username: str, password: str)->bool:
    """
    params: username: from form data, password: from form data
    summery: check admin is admin or not by username and password provided by client admin
    """
    admin = Admin.query.filter_by(username=username, password=password).first()
    if admin:
        return True
    return False


def is_admin_in_session()->bool:
    """
    summey: check "current_admin" key in session and check again with database return true if admin is found and false if not
    """
    try:
        if "current_admin" in session:
            try:
                admin = session["current_admin"]
                admin = Admin.query.filter_by(username=admin["username"], password=admin["password"]).first()
                if admin:
                    return True
                return False
            except KeyError as err:
                print(err)
                return False
    except Exception as err:
        print(err)
        return False

def is_not_valid(datas: dict) -> list:
    """
    summery: this function will take dict as arg and remove space before and after of each data and return validated list
    """
    validated_data = []
    for data in list(datas.values()):
        if data is not None and type(data) != type(int()) and type(data) != type(list()):
            validated_data.append(data.strip())
        else:
            validated_data.append(data)
    if "" in validated_data:
        return True
    if None in validated_data:
            return True
    return False