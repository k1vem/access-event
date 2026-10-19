// Скрипт демонстрационной страницы: сервер для этой страницы не используется.
function showNotification(message, isError = false) {
  const region = document.getElementById("notifications");
  if (!region) return;
  const item = document.createElement("div");
  item.className = isError ? "notification error" : "notification";
  item.setAttribute("role", isError ? "alert" : "status");
  item.textContent = message;
  region.appendChild(item);
  window.setTimeout(() => item.remove(), 4500);
}

function normalizeText(value) {
  return String(value || "").trim().toLocaleLowerCase("ru");
}

function setupEventSearch() {
  const form = document.getElementById("search-form");
  const search = document.getElementById("search");
  const filter = document.getElementById("access-filter");
  const message = document.getElementById("result-message");
  const emptyState = document.getElementById("empty-state");
  const cards = Array.from(document.querySelectorAll(".event-card"));
  const reset = document.getElementById("reset-search");
  if (!form || !search || !filter || !message || !emptyState) return;

  function updateResults() {
    let visibleCount = 0;
    cards.forEach((card) => {
      const titleMatches = normalizeText(card.dataset.title).includes(normalizeText(search.value));
      const accessMatches = !filter.value || card.dataset.access === filter.value;
      card.hidden = !(titleMatches && accessMatches);
      if (!card.hidden) visibleCount += 1;
    });
    emptyState.hidden = visibleCount !== 0;
    message.textContent = visibleCount
      ? "Найдено мероприятий: " + visibleCount + "."
      : "По вашему запросу ничего не найдено.";
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    updateResults();
  });
  search.addEventListener("input", updateResults);
  filter.addEventListener("change", updateResults);
  reset?.addEventListener("click", () => {
    form.reset();
    updateResults();
    search.focus();
  });
}

function setupDemoButtons() {
  document.querySelectorAll(".register-button").forEach((button) => {
    button.addEventListener("click", () => {
      const title = button.closest(".event-card")?.querySelector("h3")?.textContent;
      if (!title) {
        showNotification("Не удалось определить мероприятие.", true);
        return;
      }
      showNotification("Вы выбрали «" + title.trim() + "». Это демонстрация, запись не сохранена на сервере.");
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  setupEventSearch();
  setupDemoButtons();
});