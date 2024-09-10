var socket = io("");
// fetch all datas 
async function fetch_pass(in_out) {
  const dashboard_tbody = document.querySelector("#dashboard-container tbody");
  const response = await fetch("/get_all_passes");

  socket.on("pass_data", (data) => {
    // console.log(data.data)
    const today_pass = data.data;
    // const today_pass = await response.json();
    dashboard_tbody.innerHTML = '';
    var count = 1;
    today_pass.forEach(pass => {
      dashboard_tbody.innerHTML += `
          <tr>
            <td class="text-center font-bold">${count}</td>
            <td class="text-center font-bold"><img src="/static/profiles/${pass.who}/${pass.profile}" alt=""
                class="block w-20 m-auto h-20 bg-slate-300"></td>
            <td class="text-center font-bold">${pass.name}</td>
            <td class="text-center font-bold">${pass.who}</td>
            <td class="text-center font-bold">${pass.in_out}</td>
            <td class="text-center font-bold">${pass.time}</td>
            <td class="text-center font-bold flex flex-row justify-center space-x-2 aligns-center p-2">
              <a class="p-2 text-slate-200 cursor-pointer rounded-md bg-green-200 flex items-center justify-center w-fit" onclick="handleShowTimes('${pass.time_id}')">
                <img src="/static/images/clock.png" class="h-5 w-5">
              </a>
              <a class="p-2 text-slate-200 rounded-md bg-green-600 flex items-center justify-center w-fit" onclick="ViewInfo('${pass.who}', ${pass.id}, 'dashboard-container')">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M10 3a7 7 0 100 14 7 7 0 000-14zm1 8H9v2h2v-2zm0-4H9v2h2V7z" />
                </svg>
              </a>
            </td>
          </tr>
          `;
      count++;
    })
  })
}


fetch_pass("in_times");

async function handleInOut(event) {
  fetch_pass(event.target.value)
}

function fetch_rate() {
  const rates = document.querySelectorAll("#rate span");
  var index = 0;
  fetch("/rate").then(response => response.json()).then(data => {

    rates.forEach(rate => rate.innerHTML = data[rate.id] + " %")
  }).catch(error => console.error(error))

}

fetch_rate();

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