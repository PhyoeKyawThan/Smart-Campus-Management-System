async function fetchData(url) {
    const response = await fetch(url);
    if (response.ok) {
        const data = await response.json();
        return data;
    }
    throw new Error('Data fetch failed');
}

function studentCard(student) {
    return `
        <div class="max-w-xl mx-auto bg-white shadow-lg rounded-lg overflow-hidden p-4">
            <div>
                <svg class="w-4 h-4 cursor-pointer" viewBox="0 0 20 20" fill="currentColor" onclick="closeView('student-tab')">   
                    <path fill-rule="evenodd" d="M14.707 5.293a1 1 0 0 0-1.414 0L10 8.586 6.707 5.293a1 1 0 1 0-1.414 1.414L8.586 10l-3.293 3.293a1 1 0 0 0 1.414 1.414L10 11.414l3.293 3.293a1 1 0 0 0 1.414-1.414L11.414 10l3.293-3.293a1 1 0 0 0 0-1.414z" clip-rule="evenodd" />
                </svg>
            </div>
            <img src="${student.picture_uri}" class="w-48 h-48 rounded-xl block m-auto object-cover" alt="Student Picture">
            <div class="p-6">
                <h2 class="text-2xl font-semibold text-gray-800">Name: ${student.name}</h2>
                <p class="text-gray-600"><strong>Student ID:</strong> ${student.student_id}</p>
                <p class="text-gray-600"><strong>Roll No:</strong> ${student.roll_no}</p>
                <p class="text-gray-600"><strong>Current Semester:</strong> ${student.current_semester}</p>
                <p class="text-gray-600"><strong>NRC:</strong> ${student.nrc}</p>
                <p class="text-gray-600"><strong>Father's Name:</strong> ${student.father_name}</p>
                <p class="text-gray-600"><strong>Address:</strong> ${student.address}</p>
                <p class="text-gray-600"><strong>Phone No:</strong> ${student.phone_no}</p>
                <p class="text-gray-600"><strong>Email:</strong> ${student.email}</p>
                <p class="text-gray-600"><strong>Birth Date:</strong> ${student.birth_date}</p>
                <p class="text-gray-600"><strong>Register Date:</strong> ${student.register_date}</p>
            </div>
        </div>
    `;
}

function staffCard(staff) {
    return `
        <div class="max-w-sm mx-auto bg-white shadow-lg rounded-lg overflow-hidden">
            <div>
                <svg class="w-4 h-4 cursor-pointer" viewBox="0 0 20 20" fill="currentColor" onclick="closeView('staff-tab')">   
                    <path fill-rule="evenodd" d="M14.707 5.293a1 1 0 0 0-1.414 0L10 8.586 6.707 5.293a1 1 0 1 0-1.414 1.414L8.586 10l-3.293 3.293a1 1 0 0 0 1.414 1.414L10 11.414l3.293 3.293a1 1 0 0 0 1.414-1.414L11.414 10l3.293-3.293a1 1 0 0 0 0-1.414z" clip-rule="evenodd" />
                </svg>
            </div>
            <img src="${staff.picture_uri}" class="w-full h-48 object-cover" alt="Staff Picture">
            <div class="p-6">
                <h2 class="text-2xl font-semibold text-gray-800">Name: ${staff.name}</h2>
                <p class="text-gray-600"><strong>Staff ID:</strong> ${staff.staff_id}</p>
                <p class="text-gray-600"><strong>Position:</strong> ${staff.position}</p>
                <p class="text-gray-600"><strong>NRC:</strong> ${staff.nrc}</p>
                <p class="text-gray-600"><strong>Father's Name:</strong> ${staff.father_name}</p>
                <p class="text-gray-600"><strong>Address:</strong> ${staff.address}</p>
                <p class="text-gray-600"><strong>Phone No:</strong> ${staff.phone_no}</p>
                <p class="text-gray-600"><strong>Email:</strong> ${staff.email}</p>
                <p class="text-gray-600"><strong>Birth Date:</strong> ${staff.birth_date}</p>
                <p class="text-gray-600"><strong>Register Date:</strong> ${staff.register_date}</p>
            </div>
        </div>
    `;
}

function teacherCard(teacher) {
    return `
        <div class="max-w-sm mx-auto bg-white shadow-lg rounded-lg overflow-hidden">
            <div>
                <svg class="w-4 h-4 cursor-pointer" viewBox="0 0 20 20" fill="currentColor" onclick="closeView('teacher-tab')">   
                    <path fill-rule="evenodd" d="M14.707 5.293a1 1 0 0 0-1.414 0L10 8.586 6.707 5.293a1 1 0 1 0-1.414 1.414L8.586 10l-3.293 3.293a1 1 0 0 0 1.414 1.414L10 11.414l3.293 3.293a1 1 0 0 0 1.414-1.414L11.414 10l3.293-3.293a1 1 0 0 0 0-1.414z" clip-rule="evenodd" />
                </svg>
            </div>
            <img src="${teacher.picture_uri}" class="w-full h-48 object-cover" alt="Teacher Picture">
            <div class="p-6">
                <h2 class="text-2xl font-semibold text-gray-800">Name: ${teacher.name}</h2>
                <p class="text-gray-600"><strong>Teacher ID:</strong> ${teacher.teacher_id}</p>
                <p class="text-gray-600"><strong>Department:</strong> ${teacher.department}</p>
                <p class="text-gray-600"><strong>Position:</strong> ${teacher.position}</p>
                <p class="text-gray-600"><strong>NRC:</strong> ${teacher.nrc}</p>
                <p class="text-gray-600"><strong>Father's Name:</strong> ${teacher.father_name}</p>
                <p class="text-gray-600"><strong>Address:</strong> ${teacher.address}</p>
                <p class="text-gray-600"><strong>Phone No:</strong> ${teacher.phone_no}</p>
                <p class="text-gray-600"><strong>Email:</strong> ${teacher.email}</p>
                <p class="text-gray-600"><strong>Birth Date:</strong> ${teacher.birth_date}</p>
                <p class="text-gray-600"><strong>Register Date:</strong> ${teacher.register_date}</p>
            </div>
        </div>
    `;
}

function guestCard(guest) {
    return `
        <div class="max-w-sm mx-auto bg-white shadow-lg rounded-lg overflow-hidden">
            <div>
                <svg class="w-4 h-4 cursor-pointer" viewBox="0 0 20 20" fill="currentColor" onclick="closeView('guest-tab')">   
                    <path fill-rule="evenodd" d="M14.707 5.293a1 1 0 0 0-1.414 0L10 8.586 6.707 5.293a1 1 0 1 0-1.414 1.414L8.586 10l-3.293 3.293a1 1 0 0 0 1.414 1.414L10 11.414l3.293 3.293a1 1 0 0 0 1.414-1.414L11.414 10l3.293-3.293a1 1 0 0 0 0-1.414z" clip-rule="evenodd" />
                </svg>
            </div>
            <img src="${guest.picture_uri}" class="w-full h-48 object-cover" alt="Guest Picture">
            <div class="p-6">
                <h2 class="text-2xl font-semibold text-gray-800">Name: ${guest.name}</h2>
                <p class="text-gray-600"><strong>Guest Token:</strong> ${guest.token}</p>
                <p class="text-gray-600"><strong>Register Date: </strong> ${guest.register_date}</p>
            </div>
        </div>
    `;
}

function closeView(tab_id) {
    document.getElementById(tab_id).click();
}

async function ViewInfo(is_who, id, container_id) {
    let url, data, cardHTML;

    switch (is_who) {
        case 'student':
            url = `/student/get_student/${id}`;
            data = await fetchData(url);
            cardHTML = studentCard(data.student_info);
            break;
        case 'staff':
            url = `/staff/get_staff/${id}`;
            data = await fetchData(url);
            cardHTML = staffCard(data.staff_info);
            break;
        case 'teacher':
            url = `/teacher/get_teacher/${id}`;
            data = await fetchData(url);
            cardHTML = teacherCard(data.teacher_info);
            break;
        case 'guest':
            url = `/guest/get_guest/${id}`;
            data = await fetchData(url);
            cardHTML = guestCard(data.guest_info);
            break;
        default:
            cardHTML = "<h1 class='text-red-400'>Invalid category</h1>";
    }

    document.getElementById(container_id).innerHTML = cardHTML;
}
