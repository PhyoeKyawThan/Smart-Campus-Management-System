from ..models import Staff, Student, Teacher, TrackPass, Guest, Time
from flask import jsonify
from werkzeug.security import check_password_hash
import json
from .. import db
from datetime import datetime, date

def is_today_out(exist_date: datetime) -> bool:
    current = datetime.now().date()
    current_date = datetime(current.year, current.month, current.day)
    time = Time.query.filter_by(date=exist_date).first()
    if time:
        if( current_date == exist_date ):
           return True
    return False    

def student_passed_today(student_id: int) -> TrackPass:
    passes = TrackPass.query.filter_by(student_id= student_id, 
                                       date = datetime.now().date()).first()
    if passes:
        return passes
    return TrackPass()

def teacher_passed_today(teacher_id: int) -> TrackPass:
    passes = TrackPass.query.filter_by(teacher_id= teacher_id, 
                                       date = datetime.now().date()).first()
    if passes:
        return passes
    return TrackPass()

def guess_passed_today(guest_id: int) -> TrackPass:
    passes = TrackPass.query.filter_by(guest_id= guest_id, 
                                       date = datetime.now().date()).first()
    if passes:
        return passes
    return TrackPass()

def staff_passed_today(staff_id: int) -> TrackPass:
    passes = TrackPass.query.filter_by(staff_id= staff_id, 
                                       date = datetime.now().date()).first()
    if passes:
        return True
    return TrackPass()

# def response(object, format_data: dict) -> jsonify:
    

def add_trackpass(data: dict) -> bool:
    match data["who"]:
        case "student":
            student = Student.query.filter_by(roll_no=data["roll_no"]).first()
            if student:
                format_data = {
                    "student_id": student.student_id,
                    "name": student.name,
                    "roll_no": student.roll_no,
                    "father_name": student.father_name,
                    "current_semester": student.current_semester
                }
                if check_password_hash(data["token"], json.dumps(format_data)):
                    if student_passed_today(student.student_id).student_id:
                        out = Time()
                        out.out_time = datetime.now()
                        out.pass_id = student_passed_today(student_id=student.student_id).pass_id
                        db.session.add(out)
                        db.session.commit()
                    else:
                        new_pass = TrackPass()
                        new_pass.student_id = student.student_id
                        db.session.add(new_pass)
                        db.session.commit()
                        new_time = student_passed_today(student_id=student.student_id)
                        new_time.in_time = datetime.now()
                        new_time.pass_id = new_pass.pass_id
                        db.session.add(new_time)
                        db.session.commit()
                    
                    
                    return jsonify({
                        "status": 200,
                        "message": "Allowed Student",
                        "bool_val": True
                    })
            return jsonify({
                    "status": 401,
                    "message": "Unauthorized Access",
                    "bool_val": TrackPass()
                })
        case "teacher":
            teacher = Teacher.query.filter_by(teacher_id=data["teacher_id"]).first()
            if teacher:
                format_data = {
                    "teacher_id": teacher.teacher_id,
                    "name": teacher.name,
                    "father_name": teacher.father_name,
                    "nrc": teacher.nrc,
                    "birth_date": teacher.birth_date
                }
                if check_password_hash(data["token"], json.dumps(format_data)):
                    return jsonify({
                        "status": 200,
                        "message": "Allowed Teacher",
                        "bool_val": True
                    })
            return jsonify({
                    "status": 401,
                    "message": "Unauthorized Access",
                    "bool_val": TrackPass()
                })
        case "guest":
            guest = Guest.query.filter_by(guess_id=data["guess_id"]).first()
            if guest:
                format_data = {
                    "guest_id": guest.guest_id,
                    "name": guest.name,
                    "token": guest.token,
                    "register_date": guest.register_date
                }
                if check_password_hash(data["token"], json.dumps(format_data)):
                    return jsonify({
                        "status": 200,
                        "message": "Allowed Guest",
                        "bool_val": True
                    })
            return jsonify({
                    "status": 401,
                    "message": "Unauthorized Access",
                    "bool_val": TrackPass()
                })
        case "staff":
            staff = Staff.query.filter_by(staff_id = data["staff_id"]).first()
            if staff:
                format_data = {
                    "staff_id": staff.staff_id,
                    "name": staff.name,
                    "position": staff.position,
                    "father_name": staff.father_name,
                    "register_date": staff.register_date
                }
                if check_password_hash(data["token"], json.dumps(format_data)):
                    return jsonify({
                        "status": 200,
                        "message": "Allowed Teacher",
                        "bool_val": True
                    })
            return jsonify({
                    "status": 401,
                    "message": "Unauthorized Access",
                    "bool_val": TrackPass()
                })
        case _:
            return jsonify({
                    "status": 401,
                    "message": "Unauthorized Access",
                    "bool_val": TrackPass()
                })