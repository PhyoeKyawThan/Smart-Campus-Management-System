var limit = 10;
var offset = 0;
// fetch all datas 
async function fetch_guests(limit, offset, datas) {
    const guest_tbody = document.querySelector("#guest-container tbody");
    const response = await fetch(`/get_all_guest/${limit}/${offset}`);
    var guests = await response.json();
    if(datas){
        guests = datas;
    }
    var count = 1;
    guest_tbody.innerHTML = '';
    guests.forEach(guest => {
        guest_tbody.innerHTML += `
        <tr>
          <td class="text-center font-bold">${count}</td>
          <td class="text-center font-bold flex flex-row justify-center"><img src="${guest.picture_uri}" alt=""
              class="block w-20 h-20 bg-slate-300"></td>
          <td class="text-center font-bold">${guest.name}</td>
          <td class="text-center font-bold flex flex-row justify-center space-x-2 aligns-center p-2">
            <a class="p-2 text-slate-200 rounded-md bg-green-600 flex items-center justify-center w-fit" onclick="ViewInfo('guest', ${guest.guest_id}, 'guest-container')">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10 3a7 7 0 100 14 7 7 0 000-14zm1 8H9v2h2v-2zm0-4H9v2h2V7z" />
              </svg>
            </a>
            <a class="p-2 text-slate-200 rounded-md bg-red-600 flex items-center justify-center w-fit" onclick="DeleteGuest(${guest.guest_id}, 'guest-tab')">
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

fetch_guests(limit, offset, null);

async function nextRows(event) {
    offset = limit * (offset + 1);

    fetch_guests(limit, offset, null);
    // document.getElementById("prev-btn").disabled = ( offset === 0 );
}

async function previousRows(event) {
    offset -= limit; // Decrease offset by limit
    if (offset >= 0) {
        fetch_guests(limit, offset, null);
    } else {
        offset = 0; // Reset offset to 0 if it goes below 0
    }
    // Optionally disable previous button if offset is 0
}

// delete guest
async function DeleteGuest(guest_id, tab_id) {
    const tab = document.getElementById(tab_id);
    const confirm_delete = confirm("Are you sure to delete?");
    if (confirm_delete) {
        const response = await fetch(`/guest/delete/${guest_id}`, {
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

document.getElementById("search-guest-name-field").addEventListener("input", async (e) => {
    const guests = await search('/search_guest/', 'search-guest-name-field');
    limit = 10;
    offset = 0;
    fetch_guests(limit, offset, guests);
    if (e.target.value.length <= 0) {
        fetch_guests(limit, offset, null);
    }
})

var fileInput = document.getElementById("form-image");
var imagePreview = document.getElementById("imagePreview");

fileInput.addEventListener("change", function () {
    const reader = new FileReader();
    reader.onload = function () {
        imagePreview.src = reader.result;
    };
    reader.readAsDataURL(fileInput.files[0]);
});

async function addNewGuest(){
    const name = document.getElementById("guest-name");
    let data = {
        name: name.value
    };
    // first upload image
    const uploaded = uploadImage(fileInput, "guest");
    uploaded.then((result)=>{
        if(result.ok){
            data.picture_uri = result.uri;
            if(register_data("/guest/register", data)){
                alert("New Guest Added");
                name.value = "";
                imagePreview.src = "";
            }
        }else{
            return ;
        }
    })
}


