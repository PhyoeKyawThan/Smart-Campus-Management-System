// communicate with esp
async function openFunc() {
    const servo_response = await fetch("http://192.168.39.67/servo?position=180");
    if(servo_response.ok){
        const response = await servo_response.text();
        console.log(response);
    }
  }
  async function closeFunc() {
    const servo_response = await fetch("http://192.168.39.67/servo?position=0");
    if(servo_response.ok){
        const response = await servo_response.text();
        console.log(response);
    }
  }