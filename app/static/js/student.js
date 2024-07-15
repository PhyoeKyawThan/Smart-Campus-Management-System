var limit = 10;
var offset = 0;
// fetch all datas 
async function fetch_students(limit, offset, datas) {
    const student_tbody = document.querySelector("#student-container tbody");
    const response = await fetch(`/get_all_students/${limit}/${offset}`);
    var students = await response.json();
    if(datas){
        students = datas;
    }
    var count = 1;
    student_tbody.innerHTML = '';
    students.forEach(student => {
        student_tbody.innerHTML += `
        <tr>
          <td class="text-center font-bold">${count}</td>
          <td class="text-center font-bold"><img src="${student.picture_uri}" alt=""
              class="block w-20 h-20 bg-slate-300"></td>
          <td class="text-center font-bold">${student.name}</td>
          <td class="text-center font-bold">${student.current_semester}</td>
          <td class="text-center font-bold">${student.roll_no}</td>
          <td class="text-center font-bold flex flex-row justify-center space-x-2 aligns-center p-2">
            <a onclick="show_form('student-container', 'student-update-form', get_student_update_form, event)"
              data-id="${student.student_id}"
              class="p-2 text-slate-200 rounded-md bg-sky-400 flex items-center justify-center w-fit">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path
                  d="M17.414 2.586a2 2 0 00-2.828 0L14 3.172l2.828 2.828 1.586-1.586a2 2 0 000-2.828zM4 13v3h3l9.293-9.293-2.828-2.828L4 13zm-1 4a1 1 0 001 1h3a1 1 0 001-1v-1H4v1z" />
              </svg>
            </a>
            <a class="p-2 text-slate-200 rounded-md bg-green-600 flex items-center justify-center w-fit" onclick="ViewInfo('student', ${student.student_id}, 'student-container')">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10 3a7 7 0 100 14 7 7 0 000-14zm1 8H9v2h2v-2zm0-4H9v2h2V7z" />
              </svg>
            </a>
            <a class="p-2 text-slate-200 rounded-md bg-red-600 flex items-center justify-center w-fit" onclick="DeleteStudent(${student.student_id}, 'student-tab')">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M6 2a1 1 0 011-1h6a1 1 0 011 1v1H6V2zM5 4h10v1H5V4zm2 1v10a1 1 0 001 1h4a1 1 0 001-1V5H7z"
                  clip-rule="evenodd" />
              </svg>
            </a>
          </td>
        </tr>
        `;
        count++;
    })
}

fetch_students(limit, offset, null);

async function nextRows(event) {
    offset = limit * (offset + 1);
    fetch_students(limit, offset, null);
    // document.getElementById("prev-btn").disabled = ( offset === 0 );
}

async function previousRows(event) {
    offset -= limit; // Decrease offset by limit
    if (offset >= 0) {
        fetch_students(limit, offset, null);
    } else {
        offset = 0; // Reset offset to 0 if it goes below 0
    }
    // Optionally disable previous button if offset is 0
}


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


// delete student
async function DeleteStudent(student_id, tab_id) {
    const tab = document.getElementById(tab_id);
    const response = await fetch(`/student/delete/${student_id}`, {
        method: "DELETE"
    });
    const is_deleted = await response.json();
    if (is_deleted.status === 200) {
        alert(is_deleted.message);
        tab.click();
    } else {
        alert(is_deleted.message);
    }
}

document.getElementById("search-roll-no-field").addEventListener("input", async (e)=>{
    const students = await search('/search_student/', 'search-roll-no-field');
    limit = 10;
    offset = 0;
    fetch_students(limit, offset, students);
    if(e.target.value.length <= 0){
        fetch_students(limit, offset, null);
    }
})