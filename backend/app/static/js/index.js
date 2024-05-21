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
}

function viewAll() {
  document.getElementById("list-section").click();
}

async function openControl() {
  const response = await fetch("/controller");
  if (response.ok) {
    const content_data = await response.text();
    document.getElementById("Control").innerHTML = content_data;
  }
}
