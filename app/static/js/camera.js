const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const resultDiv = document.getElementById('result');
const canvasContext = canvas.getContext('2d');
let lastCode = null;
let waiting = false;

function startVideoStream() {
    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
        .then((stream) => {
            video.srcObject = stream;
            video.setAttribute('playsinline', true); // required for iOS Safari
            video.play();
            requestAnimationFrame(tick);
            resultDiv.innerText = 'Ready to scan QR codes.';
        })
        .catch((error) => {
            resultDiv.innerText = 'Error accessing camera: ' + error.message;
        });
}

async function moveServo(position) {
    try {
        const response = await fetch(`http://192.168.248.67/move?state=open`);
        if (!response.ok) throw new Error('Servo move failed');
        return response.text();
    } catch (error) {
        console.error(error);
    }
}

async function handleQRCode(code) {
    if (code.data !== lastCode) {
        lastCode = code.data;
        resultDiv.innerText = `Detected QR Code: ${code.data}`;
        try {
            const response = await fetch("/controller/who_pass?data=" + encodeURIComponent(code.data), {
                method: "POST"
            });
            if (response.ok) {
                const text = await response.json();
                if (text.status) await moveServo('0');
                console.log(text);
            } else {
                console.error('Server response was not OK.');
            }
        } catch (error) {
            console.error('Error handling QR code:', error);
        }
    }
}

function tick() {
    if (!waiting && video.readyState === video.HAVE_ENOUGH_DATA) {
        canvas.height = video.videoHeight;
        canvas.width = video.videoWidth;
        canvasContext.drawImage(video, 0, 0, canvas.width, canvas.height);

        const imageData = canvasContext.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, imageData.width, imageData.height, {
            inversionAttempts: 'dontInvert',
        });

        if (code) {
            drawBoundingBox(code.location);
            handleQRCode(code);
            waiting = true;
            setTimeout(() => {
                waiting = false;
                lastCode = null;
                console.log("Waited for 3 seconds, ready to scan again.");
            }, 3000);
        } else {
            resultDiv.innerText = 'No QR code detected.';
        }
    }
    requestAnimationFrame(tick);
}

function drawBoundingBox(location) {
    const { topLeftCorner, topRightCorner, bottomRightCorner, bottomLeftCorner } = location;
    drawLine(topLeftCorner, topRightCorner, '#FF3B58');
    drawLine(topRightCorner, bottomRightCorner, '#FF3B58');
    drawLine(bottomRightCorner, bottomLeftCorner, '#FF3B58');
    drawLine(bottomLeftCorner, topLeftCorner, '#FF3B58');
}

function drawLine(begin, end, color) {
    canvasContext.beginPath();
    canvasContext.moveTo(begin.x, begin.y);
    canvasContext.lineTo(end.x, end.y);
    canvasContext.lineWidth = 4;
    canvasContext.strokeStyle = color;
    canvasContext.stroke();
}

startVideoStream();