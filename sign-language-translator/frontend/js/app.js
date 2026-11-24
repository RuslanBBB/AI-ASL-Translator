import "./camera.js";

const transcript = document.getElementById("transcript");
const suggestions = document.getElementById("suggestions");
const clearText = document.getElementById("clear-text");
const demoToggle = document.getElementById("demo-toggle");
const demoControls = document.getElementById("demo-controls");

// Небольшой словарь для проверки интерфейса подсказок.
const demoWords = [
    "ABOUT", "ABLE", "ABOVE", "ACT", "ADD", "AFTER", "AGAIN", "ALSO", "AND", "APPLE", "ASK",
    "BACK", "BAD", "BALL", "BANANA", "BE", "BECAUSE", "BEST", "BOOK", "BOTH", "BUT",
    "CAB", "CALL", "CAN", "CAT", "CAKE", "COME", "COOL",
    "GOOD", "HAND", "HELLO", "HELP", "HOW", "LEARN", "LANGUAGE", "SIGN", "THANKS", "TODAY",
];

function updateTranscript() {
    clearText.disabled = transcript.value.length === 0;
    const prefix = transcript.value.match(/\b[a-z]+$/i)?.[0].toUpperCase();
    const matches = prefix
        ? demoWords.filter((word) => word.startsWith(prefix) && word !== prefix).slice(0, 3)
        : [];

    suggestions.replaceChildren();
    suggestions.hidden = matches.length === 0;

    for (const word of matches) {
        const choice = document.createElement("button");
        choice.type = "button";
        choice.className = "button button-outline suggestion";
        choice.textContent = word;
        choice.addEventListener("click", () => {
            transcript.value = transcript.value.replace(/\b[a-z]+$/i, word + " ");
            transcript.focus();
            updateTranscript();
        });
        suggestions.append(choice);
    }
}

transcript.addEventListener("input", updateTranscript);
clearText.addEventListener("click", () => {
    transcript.value = "";
    transcript.focus();
    updateTranscript();
});
demoToggle.addEventListener("click", () => {
    demoControls.hidden = !demoControls.hidden;
    demoToggle.setAttribute("aria-expanded", String(!demoControls.hidden));
    demoToggle.textContent = demoControls.hidden ? "Попробовать демо" : "Закрыть демо";
});
for (const letter of demoControls.querySelectorAll("[data-demo-letter]")) {
    letter.addEventListener("click", () => {
        transcript.value += letter.dataset.demoLetter;
        updateTranscript();
    });
}
updateTranscript();

const signs = {
    A: "Сожми пальцы в кулак. Большой палец оставь сбоку, вдоль указательного.",
    B: "Выпрями четыре пальца и держи их вместе. Большой палец согни поперёк ладони.",
    C: "Согни пальцы и большой палец так, чтобы кисть напоминала букву C. Оставь между ними просвет.",
};
const letters = Object.keys(signs);
const storageKey = "aslt.learned-signs.v1";
const progressNote = document.getElementById("progress-note");
const progressBar = document.getElementById("progress-bar");
const progressValue = document.getElementById("progress-value");
const navProgress = document.getElementById("nav-progress");
const trainingImage = document.getElementById("training-image");
const trainingLetter = document.getElementById("training-letter");
const trainingDescription = document.getElementById("training-description");
const learnSign = document.getElementById("learn-sign");

let selected = letters[0];
const learned = new Set();
try {
    const saved = JSON.parse(localStorage.getItem(storageKey) ?? "[]");
    if (Array.isArray(saved)) {
        saved.filter((letter) => letters.includes(letter)).forEach((letter) => learned.add(letter));
    }
} catch {
    progressNote.textContent = "Прогресс доступен до закрытия страницы.";
}

function renderTraining() {
    trainingLetter.textContent = selected;
    trainingImage.src = "assets/sign-" + selected + ".webp";
    trainingImage.alt = "Положение руки для буквы " + selected;
    trainingDescription.textContent = signs[selected];

    const isLearned = learned.has(selected);
    learnSign.setAttribute("aria-pressed", String(isLearned));
    learnSign.textContent = isLearned ? "Снять отметку" : "Отметить как выученную";

    progressBar.max = letters.length;
    progressBar.value = learned.size;
    progressValue.textContent = learned.size + " из " + letters.length;
    navProgress.textContent = learned.size + "/" + letters.length;

    for (const marker of document.querySelectorAll("[data-status-for]")) {
        const done = learned.has(marker.dataset.statusFor);
        marker.textContent = done ? "Выучено" : "В тренировку";
        marker.classList.toggle("is-learned", done);
    }
}

for (const card of document.querySelectorAll("[data-sign]")) {
    card.addEventListener("click", () => {
        selected = card.dataset.sign;
        renderTraining();
        document.getElementById("training").scrollIntoView();
        learnSign.focus({ preventScroll: true });
    });
}
document.getElementById("next-sign").addEventListener("click", () => {
    selected = letters[(letters.indexOf(selected) + 1) % letters.length];
    renderTraining();
});
learnSign.addEventListener("click", () => {
    if (learned.has(selected)) {
        learned.delete(selected);
    } else {
        learned.add(selected);
    }

    try {
        localStorage.setItem(storageKey, JSON.stringify([...learned]));
        progressNote.textContent = "Прогресс хранится в этом браузере.";
    } catch {
        progressNote.textContent = "Прогресс доступен до закрытия страницы.";
    }
    renderTraining();
});

renderTraining();
