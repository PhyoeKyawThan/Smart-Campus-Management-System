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
      if (data.status === 200) {
        alert_container.innerHTML = data.message;
      }
      alert_container.innerHTML = data.message;
    })
    .catch((err) => console.error(err));
}
