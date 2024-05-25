let campus = "";
// logout
function logout() {
  window.location.href = "/auth/admin/logout";
}
// communicate with esp
async function openFunc() {
  const servo_response = await fetch("http://192.168.39.67/servo?position=180");
  if (servo_response.ok) {
    const response = await servo_response.text();
    console.log(response);
  }
}
async function closeFunc() {
  const servo_response = await fetch("http://192.168.39.67/servo?position=0");
  if (servo_response.ok) {
    const response = await servo_response.text();
    console.log(response);
  }
}

function openNav(evt, navName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(navName).style.display = "block";
  const search = document.querySelector(".search");
  document.getElementById("Dashboard").style.display === "block"
    ? (search.style.display = "none")
    : (search.style.display = "block");
  localStorage.setItem("current_display", navName);
  evt.currentTarget.className += " active";
}

// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();
document.getElementById("defaultOpenGate").click();
document.getElementById("defaultOpenList").click();

function openCampusSection(sectionName, parentName) {
  var i, campusSections;
  campusSections = document.querySelectorAll(
    "#" + parentName + " .campus-section"
  );
  for (i = 0; i < campusSections.length; i++) {
    campusSections[i].style.display = "none";
  }
  document.getElementById(sectionName).style.display = "block";
  if( sectionName === "CampusIn" || sectionName === "CampusOut"){
    campus = sectionName;
  }
}

function viewAll() {
  document.getElementById("gate-section").click();
}

async function openControl() {
  const response = await fetch("/controller");
  if (response.ok) {
    const content_data = await response.text();
    document.getElementById("Control").innerHTML = content_data;
  }
}

function searchPass() {
  const date = document.getElementById("search-by-date").value;
  fetch("/search_by_date", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      date: date,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      // check campus in or campus out is clicked
      const campus_in = document.getElementById("in-body");
      const campus_out = document.getElementById("out-body");
      if (data.success) {

        console.log(campus);
        campus === "CampusIn"
          ? (campus_in.innerHTML = "")
          : (campus_out.innerHTML = "");
          console.log(data)
        data.data.forEach((pass) => {
          if (pass.in_time && campus === "CampusIn" ) {
            campus_in.innerHTML += `
          <tr>
          <td>${pass.pass_id}</td>
          <td><img src='${pass.profile_uri}' width="50" height="50" /></td>
          <td>${pass.name}</td>
          <td>${pass.date}</td>
          <td> In - ${pass.in_time}</td>
          <td><a href="">View</a></td>
         </tr>
          `;
          }
          
          if(pass.out_time && campus === "CampusOut"){
            campus_out.innerHTML += `
          <tr>
          <td>${pass.pass_id}</td>
          <td><img src='${pass.profile_uri}' width="50" height="50" /></td>
          <td>${pass.name}</td>
          <td>${pass.date}</td>
          <td>Out - ${pass.out_time}</td>
          <td><a href="">View</a></td>
         </tr>
          `;
          }
        });
      }
    })
    .catch((err) => console.error(err));
}
