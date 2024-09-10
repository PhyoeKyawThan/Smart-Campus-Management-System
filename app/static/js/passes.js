var pass_datas;

// fetch all datas 
async function fetch_pass(who, datas, in_out) {
  const pass_tbody = document.querySelector("#pass-container tbody");
  var passes = await fetch_pass_data(who);
  pass_datas = passes;
  // console.log(pass_datas);
  if (datas) {
    passes = datas;
  }
  pass_tbody.innerHTML = '';
  var count = 1;
  var who_id = who + "_id";

  passes.forEach(pass => {
      pass_tbody.innerHTML += `
        <tr>
          <td class="text-center font-bold">${count}</td>
          <td class="text-center font-bold"><img src="/static/profiles/${pass.who}/${pass.profile}" alt=""
              class="block w-20 m-auto h-20 bg-slate-300"></td>
          <td class="text-center font-bold">${pass.name}</td>
          <td class="text-center font-bold">${pass.who}</td>
          <td class="text-center font-bold">${pass.in_out}</td>
          <td class="text-center font-bold">${pass.date}</td>
          <td class="text-center font-bold">${pass.time}</td>
          <td class="text-center font-bold flex flex-row justify-center space-x-2 aligns-center p-2">
            <a class="p-2 text-slate-200 cursor-pointer rounded-md bg-green-200 flex items-center justify-center w-fit" onclick="handleShowTimes('${pass.time_id}')">
              <img src="/static/images/clock.png" class="h-5 w-5">
            </a>
            <a class="p-2 text-slate-200 rounded-md bg-green-600 flex items-center justify-center w-fit" onclick="ViewInfo('${pass.who}', ${pass.id}, 'pass-container')">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10 3a7 7 0 100 14 7 7 0 000-14zm1 8H9v2h2v-2zm0-4H9v2h2V7z" />
              </svg>
            </a>
          </td>
        </tr>
        `;
      count++;
  })
}

fetch_pass("student", null, "in_times");

function handleClick(event) {
  // console.log(event.target.value);
  fetch_pass(event.target.value, null, document.getElementById("in-out-option").value);
}

async function handleInOut(event) {
  const who = document.getElementById("get-who");
  fetch_pass(who.value, null, event.target.value)

}

async function fetch_pass_data(who) {
  const response = await fetch(`/get_all_passes`);
  const passes = await response.json();
  return passes;
}

var times = [];

async function ShowTimes(time_id, container_) {
  const container = document.getElementById(container_);
  const show = document.getElementById("show-time");
  const response = await fetch("/get_times/" + time_id);
  if (response.ok) {
    const data = await response.json();
    // console.log(data)
  }
}
var report_date = null;
async function search_by_date(event) {
  // const who = document.getElementById("get-who").value;
  report_date = event.target.value;
  // console.log(report_date);
  // const response = await fetch("/search_pass_by_date/" + who + "/" + event.target.value);
  // if (response.ok) {
  // const data = await response.json();
  // console.log(data)
  const datas = pass_datas.filter(pass => event.target.value === convert_date(pass.date));
  // console.log(datas);
  if (datas.length === 0) {
    alert("Not Found");
  } else {
    fetch_pass("", datas, "in_times");
  }
  // }
}

function convert_date(date_) {
  // console.log(date_);
  // const date = new Date(date_);
  // return date.toISOString().split('T')[0];
  return date_;z
}

// get report
function get_report() {
  if (report_date === null) {
    alert("Filter Date First");
    return;
  }
  window.location.href = "/get_report/" + report_date;

}

// times
function showPopup(timeDetails) {
  const popup = document.getElementById('time-popup');
  const timeDetailsContainer = document.getElementById('time-details');
  timeDetailsContainer.innerHTML = timeDetails;
  popup.classList.remove('hidden');
}

function closePopup() {
  const popup = document.getElementById('time-popup');
  popup.classList.add('hidden');
}

function handleShowTimes(timeId) {
  fetch(`/get_times/${timeId}`)
    .then(response => response.json())
    .then(data => {
      const inTimes = data.in_times.join('<br>');
      const outTimes = data.out_times.join('<br>');
      const timeDetails = `
              <h3 class="font-bold">IN Times:</h3>
              <p>${inTimes}</p>
              <h3 class="font-bold">OUT Times:</h3>
              <p>${outTimes}</p>
          `;
      showPopup(timeDetails);
    })
    .catch(error => console.error('Error fetching times:', error));
}