if(getPageFromURL() !== "dashboard"){
  openPage(getPageFromURL());
}else{
  openPage("dashboard");
}

// get page from url
function getPageFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('p') || 'dashboard';
}


function showOptions() {
  const option_container = document.getElementById("options-container");
  option_container.classList.toggle("hidden");
}
 
async function openPage(page_) {
  const container = document.getElementById("tab-content-container");
  const nav_btns = document.querySelectorAll("nav button");
  nav_btns.forEach( btn => {
    if(btn.id !== page_ + "-tab" ){ 
      btn.classList.remove("text-slate-100");
      btn.classList.remove("bg-sky-800"); 
    }else{
      btn.classList.add("text-slate-100");
      btn.classList.add("bg-sky-800");
    }
  })
  const response = await fetch("/page/" + page_);
  if (response.ok) {
    const response_ = await response.text();
    container.innerHTML = response_;
    history.pushState({}, null, `?p=${page_}`);
    reExecuteScripts(container);
  }
}

function reExecuteScripts(container) {
  const scripts = container.querySelectorAll("script");
  scripts.forEach(script => {
    // console.log("Re-executing script:", script);
    const newScript = document.createElement("script");
    if (script.src) {
      newScript.src = script.src;
    } else {
      newScript.textContent = script.textContent;
    }
    document.body.appendChild(newScript).parentNode.removeChild(newScript);
  });
}

function show_form(main_container_id, form_id, fill_form_function, event) {
  const main_ = document.getElementById(main_container_id);
  const form_ = document.getElementById(form_id);
  main_.classList.add("hidden");
  form_.classList.remove("hidden");
  fill_form_function(Number(event.currentTarget.dataset.id));
}

function close_form(main_container_id, form_id) {
  const main_ = document.getElementById(main_container_id);
  const form_ = document.getElementById(form_id);
  main_.classList.remove("hidden");
  form_.classList.add("hidden");
}



// image upload
async function uploadImage(fileInput, is_who) {
  const formData = new FormData();
  formData.append('image', fileInput.files[0]);

  try {
    const response = await fetch(`/file/upload/${is_who}`, {
      method: 'POST',
      body: formData
    });

    const result = await response.json();
    return {
      ok: response.ok,
      uri: result.image_uri,
      message: result.message
    };
  } catch (error) {
    console.error('Error uploading image:', error);
    return {
      ok: false,
      message: 'Error uploading image'
    };
  }
}

async function update_data(update_endpoint, data_object){
  const response = await fetch(update_endpoint, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data_object)
  });
  if(response.ok){
    return true;
  }
  return false;
}

async function register_data(update_endpoint, data_object){
  const response = await fetch(update_endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data_object)
  });
  if(response.ok){
    return true;
  }
  return false;
}

async function search(end_point, input_id){
  const value = document.getElementById(input_id);
  const response = await fetch(end_point + value.value);
  if(response.ok){
    return await response.json();
  }
  return [];
}