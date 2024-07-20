// fetch all datas 
async function fetch_pass(who, datas, in_out) {
  const pass_tbody = document.querySelector("#pass-container tbody");
  const passes = await fetch_pass_data(who);
  if (datas) {
    passes = datas;
  }
  pass_tbody.innerHTML = '';
  var count = 1;
  var who_id = who + "_id";
  console.log(passes);
  passes.forEach(pass => {
    pass_tbody.innerHTML += `
        <tr>
          <td class="text-center font-bold">${count}</td>
          <td class="text-center font-bold"><img src="${pass.info.picture_uri}" alt=""
              class="block w-20 m-auto h-20 bg-slate-300"></td>
          <td class="text-center font-bold">${pass.info.name}</td>
          <td class="text-center font-bold">${pass.info.who}</td>
          <td class="text-center font-bold">${pass[in_out][0] ? pass[in_out][0] : "-"}</td>
          <td class="text-center font-bold flex flex-row justify-center space-x-2 aligns-center p-2">
            <a class="p-2 text-slate-200 cursor-pointer rounded-md bg-green-200 flex items-center justify-center w-fit" onclick="ShowTimes(${pass},'pass-container')">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="currentColor"
                class="w-6 h-6 text-gray-500"
              >
                <path
                  fill-rule="evenodd"
                  d="M12 4.5a7.5 7.5 0 100 15 7.5 7.5 0 000-15zm0 13a5.5 5.5 0 110-11 5.5 5.5 0 010 11z"
                  clip-rule="evenodd"
                />
                <path
                  fill-rule="evenodd"
                  d="M12.75 7.75a.75.75 0 00-1.5 0v4a.75.75 0 00.408.671l2.5 1.25a.75.75 0 10.684-1.342l-2.092-1.046V7.75z"
                  clip-rule="evenodd"
                />
                  </svg>
            </a>
            <a class="p-2 text-slate-200 rounded-md bg-green-600 flex items-center justify-center w-fit" onclick="ViewInfo('${who}', ${pass.info[who_id]}, 'pass-container')">
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
  const response = await fetch(`/get_passes/${who}`);
  const passes = await response.json();
  return passes;
}

function ShowTimes(pass_obj, container_){
  const container = document.getElementById(container_);
  const show_time_container = document.getElementById("show-time");
  container.classList.add("hidden");
  show_time_container.classList.remove("hidden");
  console.log(pass_obj);

}