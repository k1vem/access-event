// Небольшие интерактивные функции для учебной страницы AccessEvent.
function showNotification(message, isError = false) {
  const region = document.getElementById("notifications");
  if (!region) return;

  const item = document.createElement("div");
  item.className = isError ? "notification error" : "notification";
  item.setAttribute("role", isError ? "alert" : "status");
  item.textContent = message;
  region.appendChild(item);

  window.setTimeout(() => item.remove(), 4000);
}

document.addEventListener("DOMContentLoaded", () => {
  const searchForm = document.getElementById("search-form");
  const searchInput = document.getElementById("search");
  const cards = Array.from(document.querySelectorAll(".event-card"));
  const resultMessage = document.getElementById("result-message");

  // Поиск мероприятий по названию.
  searchForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const query = searchInput.value.trim().toLocaleLowerCase("ru");
    let visibleCount = 0;

    cards.forEach((card) => {
      const title = card.dataset.title.toLocaleLowerCase("ru");
      const isVisible = title.includes(query);
      card.hidden = !isVisible;
      if (isVisible) visibleCount += 1;
    });

    resultMessage.textContent = visibleCount
      ? "Найдено мероприятий: " + visibleCount
      : "По вашему запросу ничего не найдено.";
  });

  // Демонстрация записи: на учебной странице данные не сохраняются на сервере.
  document.querySelectorAll(".register-button").forEach((button) => {
    button.addEventListener("click", () => {
      const card = button.closest(".event-card");
      const title = card.querySelector("h3").textContent;
      showNotification("Демонстрация: вы выбрали мероприятие «" + title + "». Для настоящей записи нужен сервер.");
    });
  });
});
