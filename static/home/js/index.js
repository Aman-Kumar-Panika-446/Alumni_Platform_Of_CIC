const container = document.getElementById('floating-alumni');
let currentIndex = 0;

function random(min, max) { return Math.random() * (max - min) + min; }

function createAlumni() {
  if (!alumniData || alumniData.length === 0) return;

  // Pick next alumni (loop through all)
  const imgSrc = alumniData[currentIndex];
  currentIndex = (currentIndex + 1) % alumniData.length;

  const div = document.createElement('div');
  div.className = 'alumni';
  const img = document.createElement('img');
  img.src = imgSrc;
  div.appendChild(img);

  const containerW = container.offsetWidth;
  const containerH = container.offsetHeight;

  const side = Math.floor(Math.random() * 4);
  let startX, startY, endX, endY;

  switch(side) {
    case 0: // top
      startX = random(0, containerW - 80);
      startY = -80;
      endX = random(-100, 100);
      endY = containerH + 80;
      break;
    case 1: // bottom
      startX = random(0, containerW - 80);
      startY = containerH + 80;
      endX = random(-100, 100);
      endY = -80;
      break;
    case 2: // left
      startX = -80;
      startY = random(0, containerH - 80);
      endX = containerW + 80;
      endY = random(-50, 50);
      break;
    default: // right
      startX = containerW + 80;
      startY = random(0, containerH - 80);
      endX = -80;
      endY = random(-50, 50);
  }

  div.style.left = startX + 'px';
  div.style.top = startY + 'px';
  container.appendChild(div);

  const duration = random(6, 10) * 1000;
  div.animate([
    { transform: 'translate(0,0)', opacity: 1 },
    { transform: `translate(${endX}px, ${endY}px)`, opacity: 0 }
  ], { duration: duration, easing: 'linear' });

  setTimeout(() => div.remove(), duration);
}

// Spawn one every 1.2s
setInterval(createAlumni, 1200);

// Start with a few initially
for (let i = 0; i < 10; i++) createAlumni();
