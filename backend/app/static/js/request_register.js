function requestRegister(url, datas, alert_container) {
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(datas),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      if (data.status === 200) {
        alert_container.innerHTML = data.message;
        return true;
      }
      alert_container.innerHTML = data.message;
      return true;
    })
    .catch((err) => console.error(err));
    return false;
}

async function uploadImage(image_container) {
  if (image_container.files[0]) {
    const formData = new FormData();
    formData.append("image", image_container.files[0]);
    const response = await fetch("/file/upload", {
      method: "POST",
      body: formData,
    });
    if (response.ok) {
      const response_data = await response.json();
      return {
        ok: true,
        uri: response_data.image_uri
      };
    }
    return {
      ok: false,
    };
  }
}
