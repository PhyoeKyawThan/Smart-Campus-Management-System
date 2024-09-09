var limit = 10;
var offset = 0;
var track = 0;
// fetch all datas 
async function fetch_staff(limit, offset, datas) {
    const staff_tbody = document.querySelector("#staff-container tbody");
    const response = await fetch(`/get_all_staff/${limit}/${offset}`);
    var staffs = await response.json();
    if(staffs.length === 0 ){
        track = 0;
        return;
    }
    if (datas) {
        staffs = datas;
    }
    var count = 1;
    staff_tbody.innerHTML = '';
    staffs.forEach(staff => {
        staff_tbody.innerHTML += `
        <tr>
          <td class="text-center font-bold">${count}</td>
          <td class="text-center font-bold"><img src="/static/profiles/staff/${staff.picture_uri}" alt=""
              class="block w-20 h-20 bg-slate-300"></td>
          <td class="text-center font-bold">${staff.name}</td>
          <td class="text-center font-bold">${staff.nrc}</td>
          <td class="text-center font-bold">${staff.position}</td>
          <td class="text-center font-bold">${staff.register_date}</td>
          
          <td class="text-center font-bold flex flex-row justify-center space-x-2 aligns-center p-2">
            <a onclick="show_form('staff-container', 'staff-update-form', get_staff_update_form, event)"
              data-id="${staff.staff_id}"
              class="p-2 text-slate-200 rounded-md bg-sky-400 flex items-center justify-center w-fit">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path
                  d="M17.414 2.586a2 2 0 00-2.828 0L14 3.172l2.828 2.828 1.586-1.586a2 2 0 000-2.828zM4 13v3h3l9.293-9.293-2.828-2.828L4 13zm-1 4a1 1 0 001 1h3a1 1 0 001-1v-1H4v1z" />
              </svg>
            </a>
            <a class="p-2 text-slate-200 rounded-md bg-green-600 flex items-center justify-center w-fit" onclick="ViewInfo('staff', ${staff.staff_id}, 'staff-container')">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10 3a7 7 0 100 14 7 7 0 000-14zm1 8H9v2h2v-2zm0-4H9v2h2V7z" />
              </svg>
            </a>
            <a class="p-2 text-slate-200 rounded-md bg-red-600 flex items-center justify-center w-fit" onclick="DeleteStaff(${staff.staff_id}, 'staff-tab')">
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

fetch_staff(limit, offset, null);

async function nextRows(event) {
    track += 1;
    offset = limit * track;
    fetch_staff(limit, offset, null);
}

async function previousRows(event) {
    if (offset >= 0 && track > 0) {
        track -= 1; // Decrease offset by limit
        offset = limit * track;
        fetch_staff(limit, offset, null);
    } else {
        track = 0;
        offset = 0; // Reset offset to 0 if it goes below 0
    }
    // Optionally disable previous button if offset is 0
}


// student actions
// Function to fetch staff data by ID
async function get_staff_update_form(staff_id) {
    const container = document.getElementById("staff-container");
    container.innerHTML = loader(); // Show loader while fetching data

    // Fetch staff data by ID
    const response = await fetch(`/staff/get_staff/${staff_id}`);
    if (response.ok) {
        const staff_data = await response.json();
        fill_staff_update_form(staff_data.staff_info); // Fill form with fetched data
    } else {
        console.error("Failed to fetch staff data");
    }
}

// Function to fill update form with staff data
function fill_staff_update_form(staff_data) {
    // Set image preview
    const imagePreview = document.getElementById('imagePreview');
    console.log(staff_data);
    imagePreview.src = "/static/profiles/staff/" + staff_data.picture_uri;

    // Set input fields
    document.getElementById('staffId').value = staff_data.staff_id;
    document.getElementById('fullName').value = staff_data.name;
    document.getElementById('position').value = staff_data.position;
    document.getElementById('nrc').value = staff_data.nrc;
    document.getElementById('fathersName').value = staff_data.father_name;
    document.getElementById('address').value = staff_data.address;
    document.getElementById('emailAddress').value = staff_data.email;
    document.getElementById('phoneNumber').value = staff_data.phone_no;
    document.getElementById('birthDate').value = new Date(staff_data.birth_date).toISOString().split('T')[0];
}

// Function to validate and submit form data
function validateForm(event) {
    event.preventDefault();

    // Retrieve form data
    const data = {
        staff_id: document.getElementById("staffId").value,
        name: document.getElementById("fullName").value,
        position: document.getElementById("position").value,
        nrc: document.getElementById("nrc").value,
        father_name: document.getElementById("fathersName").value,
        address: document.getElementById("address").value,
        email: document.getElementById("emailAddress").value,
        phone_no: document.getElementById("phoneNumber").value,
        birth_date: document.getElementById("birthDate").value,
    };

    // Implement your validation logic here
}




// Other functions for image preview, form validation, etc. (as per your requirements)

// validating form

// Function to validate and submit staff update form
function staffValidateForm(event) {
    event.preventDefault();

    // Form field values
    const staffId = document.getElementById("staffId").value.trim();
    const fullName = document.getElementById("fullName").value.trim();
    const nrc = document.getElementById("nrc").value.trim();
    const position = document.getElementById("position").value.trim();
    const fathersName = document.getElementById("fathersName").value.trim();
    const address = document.getElementById("address").value.trim();
    const emailAddress = document.getElementById("emailAddress").value.trim();
    const phoneNumber = document.getElementById("phoneNumber").value.trim();
    const birthDate = document.getElementById("birthDate").value.trim();
    const fileInput = document.getElementById("form-image");

    // Prepare data object for submission
    const data = {
        staff_id: staffId,
        name: fullName,
        nrc: nrc,
        position: position,
        father_name: fathersName,
        address: address,
        email: emailAddress,
        phone_no: phoneNumber,
        birth_date: birthDate,
    };

    // Handle image upload if a file is selected
    if (fileInput.files && fileInput.files[0]) {
        uploadImage(fileInput, 'staff')
            .then((result) => {
                if (result.ok) {
                    data.picture_uri = result.uri;
                    // Call update function with image URI included
                    update_staff_data(data);
                }
            })
            .catch((err) => console.error(err));
    } else {
        // Call update function without image URI
        update_staff_data(data);
    }
}

function update_staff_data(data) {
    // Assuming you have an update API endpoint '/staff/update'
    fetch('/staff/update_staff/' + data.staff_id, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => {
            if (response.ok) {
                alert("Staff information updated successfully.");
                // Additional actions after successful update
            } else {
                alert("Failed to update staff information. Please try again.");
            }
        })
        .catch(error => {
            console.error('Error updating staff information:', error);
            alert("Failed to update staff information. Please try again.");
        });
}
// Function to handle image preview when file input changes
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
async function DeleteStaff(staff_id, tab_id) {
    const tab = document.getElementById(tab_id);
    const confirm_delete = confirm("Are you sure to delete?");
    if (confirm_delete) {
        const response = await fetch(`/staff/delete/${staff_id}`, {
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
}

document.getElementById("search-staff-name-field").addEventListener("input", async (e) => {
    const staffs = await search('/search_staff/', 'search-staff-name-field');
    limit = 10;
    offset = 0;
    fetch_staff(limit, offset, staffs);
    if (e.target.value.length <= 0) {
        fetch_staff(limit, offset, null);
    }
})