// student actions
async function get_student_update_form(student_id) {
    const container = document.getElementById("student-container");
    container.innerHTML = loader();
    const response = await fetch(`/student/get_student/${student_id}`);
    if (response.ok) {
        // container.removeChild(document.getElementById("loader"));
        const student_data = await response.json();
        console.log(student_data);
        fill_student_update_form(student_data.student_info);
    }
}

function fill_student_update_form(student_data) {
    // Set image preview
    const imagePreview = document.getElementById('imagePreview');
    imagePreview.src = student_data.picture_uri;

    // Set input fields
    document.getElementById('studentId').value = student_data.student_id;
    document.getElementById('fullName').value = student_data.name;
    document.getElementById('rollNo').value = student_data.roll_no;
    document.getElementById('nrc').value = student_data.nrc;
    document.getElementById('currentSemester').value = student_data.current_semester;
    document.getElementById('fathersName').value = student_data.father_name;
    document.getElementById('address').value = student_data.address;
    document.getElementById('emailAddress').value = student_data.email;
    document.getElementById('phoneNumber').value = student_data.phone_no;
    document.getElementById('birthDate').value = new Date(student_data.birth_date).toISOString().split('T')[0];
}

// validating form

function validateForm(event) {
    event.preventDefault();

    const rollNo = document.getElementById("rollNo").value.trim();
    const nrc = document.getElementById("nrc").value.trim();
    const phoneNumber = document.getElementById("phoneNumber").value.trim();

    const rollNoPattern = /^(1cst|2cs|3cs|4cs|5cs)-([1-9][0-9]?|100)$/;
    const nrcPattern = /^([1-9]|1[0-4])\/[a-zA-Z]{3}\((n|p)\)\d{6}$/;
    const phonePattern = /^(09[246789]\d{8}|(\d{4,9}))$/;

    if (!rollNoPattern.test(rollNo)) {
        alert("Invalid roll number. Roll number must be in the format like 1cst-1 to 1cst-100 and 2cs-1 to 2cs-100 and so on.");
        return false;
    }

    if (!nrcPattern.test(nrc)) {
        alert("Invalid NRC. NRC must be in the format like 14/zln(n)187660 where 14 may be 1 to 14, zln are three characters, (n) is n or p, and 187660 is six digits.");
        return false;
    }

    if (!phonePattern.test(phoneNumber)) {
        alert("Invalid phone number. Phone number must be between 4 and 9 digits, or start with 09 followed by 11 digits with the third digit being 2, 4, 6, 7, 8, or 9.");
        return false;
    }

    // datas
    const data = {
        student_id: document.getElementById("studentId").value,
        name: document.getElementById("fullName").value,
        roll_no: document.getElementById("rollNo").value,
        nrc: document.getElementById("nrc").value,
        current_semester: document.getElementById("currentSemester").value,
        father_name: document.getElementById("fathersName").value,
        address: document.getElementById("address").value,
        email: document.getElementById("emailAddress").value,
        phone_no: document.getElementById("phoneNumber").value,
        birth_date: document.getElementById("birthDate").value,
    };
    const fileInput = document.getElementById("form-image");

    if (fileInput.files && fileInput.files[0]) {
        const image_uploaded = uploadImage(document.getElementById("form-image"), 'student');
        image_uploaded
            .then((result) => {
                if (result.ok) {
                    data.picture_uri = result.uri;
                    if (update_data("/student/update_student/" + data.student_id, data)) {
                        alert("Updated");
                    }
                }
            })
            .catch((err) => console.error(err));
    } else {
        console.log(data);
        if (update_data("/student/update_student/" + data.student_id, data)) {
            alert("Updated");
        }
    }
}

var fileInput = document.getElementById("form-image");
var imagePreview = document.getElementById("imagePreview");

fileInput.addEventListener("change", function () {
    const reader = new FileReader();
    reader.onload = function () {
        imagePreview.src = reader.result;
    };
    reader.readAsDataURL(fileInput.files[0]);
});
