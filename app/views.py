from flask import Blueprint, render_template, abort, jsonify, request, Response, send_from_directory, current_app, send_file
from . import db
from .assets.validate import is_admin_in_session
from .viewModel import ViewModel
# from . import socket as socketio
from .event_ import generate
from os import path
from xhtml2pdf import pisa
import io

views = Blueprint("views", __name__)

@views.route("/test")
def test_event():
    view = ViewModel()
    return render_template("test.html")

@views.route("/get_report/<string:date>", methods=["GET"])
def print_report(date):
    if request.method == "GET":
        if not is_admin_in_session():
            return render_template("admin_login.html")
        views = ViewModel()
        # from .report import generate_pdf
        html =  render_template("report.html", times = views.get_passes_by_date(date), report_date = date)
        
        buffer = io.BytesIO()
        pisa.CreatePDF(io.StringIO(html), dest=buffer)
        buffer.seek(0)

    # Return PDF as response
    return Response(buffer, mimetype='application/pdf', headers={"Content-Disposition": f"attachment;filename=report_{date}.pdf"})

@views.route("/get_all_passes")
def get_all_passes():
    if request.method == "GET":
        if not is_admin_in_session():
            return render_template("admin_login.html")
        views = ViewModel()
        return jsonify(views.get_passes_by_date())  

# @views.route('/stream_passes/<string:who>')
# def stream(who):
    # from flask import current_app
    # return Response(generate(current_app, who), mimetype='text/event-stream')

@views.route("/")
def home():
    if not is_admin_in_session():
        return render_template("admin_login.html")
    view = ViewModel()
    return render_template("index.html",
                           students=view.get_student_info(),
                           teachers=view.get_teacher_info()) 

@views.route("/page/<string:page>")
def get_page(page: str):
    return render_template(f"{page}/index.html")


@views.route("/get_info/<string:which>")
def get_info(which):
    view = ViewModel()
    return jsonify({
        "data": view.gate_passes(which)
    })

@views.route('/camera')
def camera():
    return render_template("camera.html")

@views.route("/get_all_students/<int:limit>/<int:offset>")
def student_views(limit: int, offset: int):
    if not is_admin_in_session():
        return render_template("admin_login.html")
    view = ViewModel()
    students = view.get_student_info(limit, offset)
    return jsonify(students)

@views.route("/search_student/<string:roll_no>")
def get_student_id(roll_no):
    view = ViewModel()
    student = view.search_student_by_roll(roll_no)
    return jsonify(student)

@views.route("/register_student")
def student_register_view():
    if not is_admin_in_session():
        return render_template("admin_login.html")
    return render_template("student/register.html")
# student
@views.route("/get_all_teachers/<int:limit>/<int:offset>")
def get_all_teachers(limit: int, offset: int):
    if not is_admin_in_session():
        return render_template("admin_login.html")
    view = ViewModel()
    teachers = view.get_teacher_info(limit, offset)
    return jsonify(teachers)

@views.route("/search_teacher/<string:name>")
def search_teacher(name):
    view = ViewModel()
    teacher = view.search_teacher_by_name(name)
    return jsonify(teacher)

@views.route("/register_teacher")
def teacher_register_view():
    if not is_admin_in_session():
        return render_template("admin_login.html")
    return render_template("teacher/register.html")
# teacher



@views.route("/register_staff")
def staff_register_view():
    if not is_admin_in_session():
        return render_template("admin_login.html")
    return render_template("staff/register.html")

@views.route("/get_all_staff/<int:limit>/<int:offset>")
def get_all_staff(limit: int, offset: int):
    if not is_admin_in_session():
        return render_template("admin_login.html")
    view = ViewModel()
    staff = view.get_staff_info(limit=limit ,offset=offset)
    return jsonify(staff)

@views.route("/search_staff/<string:name>")
def search_staff(name):
    view = ViewModel()
    teacher = view.search_staff_by_name(name)
    return jsonify(teacher)
#staff
@views.route("/admin_login")
def admin_login_view():
    return render_template("admin_login.html")

@views.route("/get_passes/<string:which_>")
def get_passes(which_):
    if not is_admin_in_session():
        return render_template("admin_login.html")
    view = ViewModel()
    passes = view.gate_passes(which_)
    return jsonify(passes)

@views.route("/search_pass_by_date/<string:who>/<string:date>")
def get_passes_by_date(who: str, date):
    if not is_admin_in_session():
        return render_template("admin_login.html")
    view = ViewModel()
    return jsonify(view.gate_passes(who, date))

@views.route("/today_pass")
def today_pass():
    if not is_admin_in_session():
        return render_template("admin_login.html")
    view = ViewModel()
    return jsonify(view.today_pass())
# pass 

@views.route("/get_all_guest/<int:limit>/<int:offset>")
def get_all_guest(limit: int, offset: int):
    if not is_admin_in_session():
        return render_template("admin_login.html")
    view = ViewModel()
    staff = view.get_guest_info(limit=limit ,offset=offset)
    return jsonify(staff)

@views.route("/search_guest/<string:guest_name>")
def search_guest(guest_name):
    if not is_admin_in_session():
        return render_template("admin_login.html")
    view = ViewModel()
    guests = view.search_by_guest_name(guest_name)
    return jsonify(guests)
# guest

@views.route("/qr_token/<string:who>/<int:id>")
def get_qr_token(who: str, id: int):
    if not is_admin_in_session():
        return render_template("admin_login.html")
    from .data_generator import TokenGenerator
    token = TokenGenerator(who)
    token.generate(id)
    # return jsonify(token.DICT_TOKEN)
    token.get_qr_code(id)
    # print(current_app.config["QR_CODE_DIR"])
    return send_file(path.join("qrcodes/", path.basename(token.QR_CODE_PATH))) 

@views.route("/get_times/<int:time_id>")
def get_times(time_id):
    if not is_admin_in_session():
        return render_template("admin_login.html")
    view = ViewModel()
    return jsonify(view.get_times(time_id))


@views.route("/rate")
def rate():
    if not is_admin_in_session():
        return render_template("admin_login.html")
    view = ViewModel()
    return jsonify(view.calculate_today_passed_rate())

