async function loadLevels() {
  const host = document.getElementById("dynamic-levels");
  const template = document.getElementById("module-template");
  if (!host || !template) return;

  try {
    const res = await fetch("/api/levels");
    if (!res.ok) throw new Error(`Request failed: ${res.status}`);

    const payload = await res.json();
    host.innerHTML = "";

    payload.levels.forEach((item, index) => {
      const node = template.content.firstElementChild.cloneNode(true);
      node.querySelector(".module-title").textContent = `${item.level.toUpperCase()} (${item.count})`;
      node.querySelector(".module-summary").textContent = item.description;
      node.classList.add("reveal");
      node.style.animationDelay = `${index * 90}ms`;
      host.appendChild(node);
    });
  } catch (error) {
    host.innerHTML = `<p>Could not load database modules right now.</p>`;
    console.error(error);
  }
}

document.addEventListener("DOMContentLoaded", loadLevels);
