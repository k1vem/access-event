# AccessEvent — платформа инклюзивных мероприятий

**Автор:** Коновалова Катя, группа 22-ИС

AccessEvent — веб-платформа для организации мероприятий с акцентом на доступность для людей с нарушениями слуха. Участники могут просматривать события, регистрироваться, получать визуальные уведомления, общаться в текстовом чате и оставлять отзывы.

## Технологии
- **Backend:** Python 3.11, Flask, Flask-SQLAlchemy, JWT.
- **Frontend:** HTML5, Jinja2, CSS3, JavaScript.
- **База данных:** PostgreSQL 16 (SQLite используется для автоматических тестов).
- **Контейнеризация:** Docker, Docker Compose.
- **CI:** GitHub Actions.

## Функциональность
- Регистрация и вход по email и паролю; пароль хранится в виде хеша.
- Роли guest, user, organizer и admin.
- Каталог мероприятий, поиск и фильтрация по доступности.
- Создание мероприятий организатором.
- Заявка на участие со статусом pending; организатор может подтвердить или отменить заявку.
- Текстовый чат на странице мероприятия.
- Отзывы с оценкой от 1 до 5.
- Визуальные уведомления о статусе регистрации.
- Адаптивный интерфейс и ARIA-разметка.

## Запуск локально
Требуется Python 3.11+.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Откройте http://127.0.0.1:5000.

## Запуск через Docker
```bash
docker compose up --build
```
Откройте http://127.0.0.1:5000. В Docker Compose база доступна приложению по имени сервиса PostgreSQL, а не через localhost.

## Тесты
```bash
# macOS/Linux
TESTING=1 python -m pytest -v
# Windows PowerShell
$env:TESTING="1"; python -m pytest -v
```

## API
- `POST /api/register`, `POST /api/login` — регистрация и вход.
- `GET /api/events`, `GET /api/events/<id>`, `POST /api/events` — каталог и создание событий.
- `POST /api/events/<id>/register`, `GET /api/my/registrations`, `PATCH /api/registrations/<id>` — заявки.
- `GET/POST /api/events/<id>/messages` — текстовый чат.
- `GET/POST /api/events/<id>/reviews` — отзывы.
- `GET /api/notifications` — визуальные уведомления.

Защищённые запросы должны содержать заголовок `Authorization: Bearer <token>`.

## Структура
- `app.py`, `config.py` — Flask-приложение и конфигурация.
- `models.py` — модели данных.
- `routes/` — маршруты API.
- `utils/` — JWT, пароли и вспомогательные функции доступности.
- `templates/` — HTML-шаблоны: главная, каталог, вход, регистрация, личный кабинет и страница мероприятия.
- `static/css/style.css`, `static/js/main.js` — CSS и JavaScript интерфейса.
- `docs/` — анализ, требования, архитектура, SQL-схема и руководства.
- `tests/` — автоматизированные тесты.

