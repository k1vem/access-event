/**
 * AccessEvent — интерактивные элементы учебной страницы.
 * Данные мероприятий демонстрационные и не отправляются на сервер.
 */

/**
 * Показывает визуальное уведомление.
 * Ошибки получают отдельный стиль и роль alert для доступности.
 */
function showNotification(message, isError = false) {
  const region = document.getElementById("notifications");
  if (!region) return;

  const item = document.createElement("div");
  item.className = isError ? "notification error" : "notification";
  item.setAttribute("role", isError ? "alert" : "status");
  item.textContent = message;
  region.appendChild(item);

  // Удаляем уведомление, чтобы оно не накапливалось на экране.
  window.setTimeout(() => {
    item.remove();
  }, 4500);
}

/** Нормализует текст для поиска без учёта регистра и лишних пробелов. */
function normalizeText(value) {
  return String(value || "").trim().toLocaleLowerCase("ru");
}

/** Возвращает карточки, которые подходят под текст и фильтр доступности. */
function filterEvents(cards, query, accessType) {
  return cards.filter((card) => {
    const title = normalizeText(card.dataset.title);
    const access = card.dataset.access || "";
    const matchesTitle = title.includes(normalizeText(query));
    const matchesAccess = !accessType || access === accessType;
    return matchesTitle && matchesAccess;
  });
}

/** Обновляет список и сообщение о количестве результатов. */
function renderSearchResults(cards, matchingCards, resultMessage, emptyState) {
  cards.forEach((card) => {
    card.hidden = !matchingCards.includes(card);
  });

  if (matchingCards.length === 0) {
    resultMessage.textContent = "Мероприятия не найдены.";
    emptyState.hidden = false;
    return;
  }

  emptyState.hidden = true;
  resultMessage.textContent = "Найдено мероприятий: " + matchingCards.length + ".";
}

/** Подключает поиск, фильтр доступности и кнопку сброса. */
function setupEventSearch() {
  const form = document.getElementById("search-form");
  const searchInput = document.getElementById("search");
  const accessFilter = document.getElementById("access-filter");
  const resultMessage = document.getElementById("result-message");
  const emptyState = document.getElementById("empty-state");
  const cards = Array.from(document.querySelectorAll(".event-card"));
  const resetButton = document.getElementById("reset-search");

  // Если на странице нет блока афиши, поисковые обработчики не нужны.
  if (!form || !searchInput || !accessFilter || !resultMessage || !emptyState) {
    return;
  }

  const updateResults = () => {
    const matchingCards = filterEvents(cards, searchInput.value, accessFilter.value);
    renderSearchResults(cards, matchingCards, resultMessage, emptyState);
  };

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    updateResults();
  });

  // Фильтрация также работает сразу при изменении поля.
  searchInput.addEventListener("input", updateResults);
  accessFilter.addEventListener("change", updateResults);

  resetButton?.addEventListener("click", () => {
    form.reset();
    cards.forEach((card) => {
      card.hidden = false;
    });
    emptyState.hidden = true;
    resultMessage.textContent = "Показаны все мероприятия.";
    searchInput.focus();
  });
}

/** Подключает демонстрационные кнопки выбора мероприятия. */
function setupRegistrationButtons() {
  document.querySelectorAll(".register-button").forEach((button) => {
    button.addEventListener("click", () => {
      const card = button.closest(".event-card");
      const title = card?.querySelector("h3")?.textContent?.trim();

      if (!title) {
        showNotification("Не удалось определить мероприятие.", true);
        return;
      }

      showNotification(
        "Вы выбрали мероприятие «" + title +
        "». Это демонстрация: для настоящей записи требуется сервер."
      );
    });
  });
}

/** Инициализация страницы после загрузки HTML. */
document.addEventListener("DOMContentLoaded", () => {
  setupEventSearch();
  setupRegistrationButtons();
});