# AccessEvent — платформа инклюзивных мероприятий

**Автор:** Коновалова Катя, группа 22-ИС

AccessEvent — веб-платформа для организации мероприятий с акцентом на доступность для людей с нарушениями слуха. Участники могут просматривать события, регистрироваться, получать визуальные уведомления, общаться в текстовом чате и оставлять отзывы.

## Технологии
- **Backend:** Python 3.11, Flask, Flask-SQLAlchemy, JWT.
- **Frontend:** HTML5, Jinja2, CSS3, JavaScript.
- **База данных:** PostgreSQL 16 в Docker Compose; SQLite для автоматических тестов и локального запуска по умолчанию.
- **Контейнеризация:** Docker, Docker Compose.
- **CI/CD:** GitHub Actions.

## Функциональность
- Регистрация и вход по email и паролю; пароль хранится в виде хеша.
- Роли user, organizer и admin; каталог доступен без авторизации.
- Каталог мероприятий, поиск и фильтрация по доступности.
- Создание мероприятий организатором.
- Заявка на участие со статусом pending; организатор может подтвердить или отменить заявку.
- Текстовый чат на странице мероприятия через API.
- Отзывы с оценкой от 1 до 5.
- Визуальные уведомления о статусе регистрации.
- Адаптивный интерфейс, подписи полей и ARIA-разметка.

## Запуск локально
Требуется Python 3.11+.

1. Создайте виртуальное окружение:
   ```bash
   python -m venv .venv
   ```
2. Активируйте его:
   - Windows PowerShell: `.venv\\Scripts\\Activate.ps1`
   - macOS/Linux: `source .venv/bin/activate`
3. Установите зависимости: `python -m pip install -r requirements.txt`.
4. При необходимости скопируйте `.env.example` в `.env` и замените секреты на случайные значения. Без `DATABASE_URL` приложение использует локальную SQLite.
5. Запустите: `python app.py`.
6. Откройте http://127.0.0.1:5000.

## Запуск через Docker
Из корня репозитория выполните:

```bash
docker compose up --build
```

Откройте http://127.0.0.1:5000. Compose запускает PostgreSQL и ждёт готовности базы перед стартом приложения. Для остановки нажмите Ctrl+C, затем выполните `docker compose down`. Данные PostgreSQL хранятся в Docker volume.

## Тесты
Из корня проекта выполните:

```bash
python -m pytest -v
```

Тестовая конфигурация использует SQLite in-memory и не требует запущенного PostgreSQL.

## Основные API-маршруты
- `POST /api/auth/register`, `POST /api/auth/login` — регистрация и вход.
- `GET /api/events`, `GET /api/events/<id>`, `POST /api/events` — каталог, карточка и создание мероприятия.
- `POST /api/events/<id>/register`, `DELETE /api/events/<id>/register`, `GET /api/me/registrations`, `PATCH /api/registrations/<id>` — заявки.
- `GET/POST /api/events/<id>/messages` — текстовый чат.
- `GET/POST /api/events/<id>/reviews` — отзывы.
- `GET /api/notifications`, `PATCH /api/notifications/<id>` — уведомления.
- `GET /health` — проверка состояния приложения.

Для защищённых запросов передавайте `Authorization: Bearer <token>`. Полный перечень описан в [docs/api.md](docs/api.md).

## Структура
- `app.py`, `config.py` — создание приложения и конфигурация.
- `models.py` — SQLAlchemy-модели.
- `routes/` — маршруты авторизации, мероприятий, регистраций и общения.
- `utils/` — JWT, хеширование паролей и функции доступности.
- `templates/` — HTML/Jinja2-страницы.
- `static/css/style.css`, `static/js/main.js` — стили и клиентский JavaScript.
- `docs/` — анализ, ТЗ, архитектура, SQL-схема, тестирование и руководства.
- `tests/` — автоматические тесты pytest.
- `.github/workflows/` — проверки этапов практики и сборка Docker-образа.

## Документы практики
Материалы по дням 1–6 собраны в каталоге [docs](docs/): анализ и ТЗ, проектирование, описание API, тест-кейсы, журнал дефектов, руководства пользователя и администратора, оценка проекта.
