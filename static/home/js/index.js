const container = document.getElementById("benzene");
const radius = 260;    // distance from center
const numAtoms = 6;    // atoms per ring

let currentSet = 0;

// === Popup elements ===
const popup = document.getElementById("popup");
const closePopup = document.getElementById("closePopup");

function showPopup(data) {
    document.getElementById("popup-img").src = data.src;
    document.getElementById("popup-name").textContent = data.name;
    document.getElementById("popup-batch").textContent = `Batch: ${data.batch}`;
    document.getElementById("popup-role").textContent = `Role: ${data.role}`;
    popup.classList.add("active");
}

closePopup.addEventListener("click", () => popup.classList.remove("active"));
popup.addEventListener("click", (e) => { 
    if (e.target === popup) popup.classList.remove("active"); 
});

// === Function to create atoms for current set ===
function createAtoms(setIndex) {
    // Remove existing atoms
    document.querySelectorAll(".atom").forEach(el => el.remove());

    const start = setIndex * numAtoms;
    const end = start + numAtoms;
    const images = alumniData.slice(start, end);

    images.forEach((imgData, i) => {
        const atom = document.createElement("div");
        atom.classList.add("atom");
        const img = document.createElement("img");
        img.src = imgData?.src || "";   // empty or invalid src
        img.onerror = function () {
        this.src = "/static/defaults/profile.png"; // default image path
        };
        atom.appendChild(img);

        // Position atoms in circle
        const angle = (i * 360) / numAtoms;
        const x = 200 + radius * Math.cos((angle * Math.PI) / 180) - 60;
        const y = 200 + radius * Math.sin((angle * Math.PI) / 180) - 60;
        atom.style.left = `${x}px`;
        atom.style.top = `${y}px`;

        // Popup on click
        atom.addEventListener("click", () => showPopup(imgData));

        // Hover → pause rotation
        atom.addEventListener("mouseenter", () => {
            container.style.animationPlayState = "paused";
            document.querySelectorAll(".atom").forEach(a => a.style.animationPlayState = "paused");
        });
        atom.addEventListener("mouseleave", () => {
            container.style.animationPlayState = "running";
            document.querySelectorAll(".atom").forEach(a => a.style.animationPlayState = "running");
        });

        container.appendChild(atom);
    });
}

// === Initialize first set ===
createAtoms(currentSet);

// === Cycle to next set after full rotation ===
container.addEventListener("animationiteration", () => {
    currentSet = (currentSet + 1) % Math.ceil(alumniData.length / numAtoms);
    createAtoms(currentSet);
});
