(function () {
  const searchInput = document.getElementById("search");
  const accessibleInput = document.getElementById("accessible");
  const resetButton = document.getElementById("reset");
  const eventCards = Array.from(document.querySelectorAll(".event-card"));
  const resultCount = document.getElementById("result-count");
  const notification = document.getElementById("notification");

  function filterEvents() {
    const searchText = searchInput.value.trim().toLocaleLowerCase("ru");
    let visibleCount = 0;
    eventCards.forEach(function (card) {
      const title = card.dataset.title.toLocaleLowerCase("ru");
      const matchesText = title.includes(searchText);
      const matchesAccess = !accessibleInput.checked || card.dataset.accessible === "true";
      const isVisible = matchesText && matchesAccess;
      card.hidden = !isVisible;
      if (isVisible) visibleCount += 1;
    });
    resultCount.textContent = "Найдено мероприятий: " + visibleCount;
  }

  searchInput.addEventListener("input", filterEvents);
  accessibleInput.addEventListener("change", filterEvents);
  resetButton.addEventListener("click", function () {
    searchInput.value = "";
    accessibleInput.checked = false;
    filterEvents();
  });
  document.querySelectorAll(".register-button").forEach(function (button) {
    button.addEventListener("click", function () {
      const title = button.closest(".event-card").dataset.title;
      notification.textContent = "Демо-запись на мероприятие «" + title + "». Данные не отправляются на сервер.";
      notification.hidden = false;
    });
  });
  filterEvents();
}());