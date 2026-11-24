const video = document.getElementById("webcam");
const frame = document.getElementById("camera-frame");
const button = document.getElementById("camera-toggle");
const buttonLabel = document.getElementById("camera-button-label");
const status = document.getElementById("camera-status");
const indicator = document.getElementById("camera-indicator");
const indicatorText = document.getElementById("camera-indicator-text");

let stream = null;
let requestVersion = 0;

function stopCamera(message = "Камера выключена.") {
    requestVersion += 1;
    stream?.getTracks().forEach((track) => track.stop());
    stream = null;
    video.srcObject = null;
    video.hidden = true;
    frame.classList.remove("is-live");
    indicator.classList.remove("is-live");
    indicatorText.textContent = "Выключена";
    buttonLabel.textContent = "Включить камеру";
    button.disabled = false;
    status.textContent = message;
}

async function startCamera() {
    if (!navigator.mediaDevices?.getUserMedia) {
        status.textContent = "Открой страницу через HTTPS или localhost для доступа к камере.";
        return;
    }

    const version = ++requestVersion;
    button.disabled = true;
    status.textContent = "Ожидаем разрешение на доступ к камере.";

    try {
        const opened = await navigator.mediaDevices.getUserMedia({
            video: { width: { ideal: 1280 }, height: { ideal: 720 } },
            audio: false,
        });

        if (version !== requestVersion) {
            opened.getTracks().forEach((track) => track.stop());
            return;
        }

        stream = opened;
        opened.getVideoTracks().forEach((track) => {
            track.addEventListener("ended", () => {
                if (stream === opened) stopCamera("Камера отключилась.");
            });
        });

        video.srcObject = opened;
        video.hidden = false;
        await video.play();
        if (version !== requestVersion) return;

        frame.classList.add("is-live");
        indicator.classList.add("is-live");
        indicatorText.textContent = "Включена";
        buttonLabel.textContent = "Выключить камеру";
        button.disabled = false;
        status.textContent = "Расположи руку в центре кадра.";
    } catch (error) {
        if (version !== requestVersion) return;

        const messages = {
            NotAllowedError: "Доступ запрещён. Разреши камеру в настройках браузера.",
            NotFoundError: "Камера не найдена. Подключи её и попробуй снова.",
            NotReadableError: "Камера недоступна. Проверь, не занята ли она другим приложением.",
        };
        stopCamera(messages[error.name] ?? "Не удалось открыть камеру. Попробуй снова.");
    }
}

button.addEventListener("click", () => {
    if (stream) {
        stopCamera();
    } else {
        startCamera();
    }
});

window.addEventListener("pagehide", () => stopCamera());
