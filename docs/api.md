# API AccessEvent

Базовый адрес при локальном запуске: `http://127.0.0.1:5000`. Данные запросов передаются в JSON. Защищённые маршруты используют заголовок `Authorization: Bearer <token>`. Токен JWT действует 24 часа по умолчанию.

## Маршруты

| Метод | Путь | Доступ | Назначение |
|---|---|---|---|
| GET | /health | Публичный | Состояние сервиса |
| POST | /api/auth/register | Публичный | Регистрация |
| POST | /api/auth/login | Публичный | Вход |
| GET | /api/events | Публичный | Каталог; параметры q и accessibility |
| GET | /api/events/{id} | Публичный | Детали мероприятия |
| POST | /api/events | organizer/admin | Создание мероприятия |
| POST | /api/events/{id}/register | Авторизованный | Запись на мероприятие |
| DELETE | /api/events/{id}/register | Авторизованный | Отмена своей записи |
| GET | /api/me/registrations | Авторизованный | Мои записи |
| PATCH | /api/registrations/{id} | organizer/admin с проверкой владельца | Изменить статус заявки |
| GET, POST | /api/events/{id}/messages | Авторизованный | Чтение и отправка сообщений |
| GET | /api/events/{id}/reviews | Публичный | Список отзывов |
| POST | /api/events/{id}/reviews | Авторизованный | Создать отзыв |
| GET | /api/notifications | Авторизованный | Мои уведомления |
| PATCH | /api/notifications/{id} | Владелец уведомления | Отметить уведомление прочитанным |

## Примеры JSON

### Регистрация — POST /api/auth/register
```json
{
  "username": "katya",
  "email": "katya@example.com",
  "password": "replace-with-a-strong-password",
  "is_deaf": false
}
```

### Вход — POST /api/auth/login
```json
{
  "email": "katya@example.com",
  "password": "replace-with-a-strong-password"
}
```

### Создание мероприятия — POST /api/events
Для запроса нужен JWT пользователя с ролью organizer или admin.

```json
{
  "title": "Лекция с субтитрами",
  "description": "Открытая лекция с текстовым сопровождением",
  "event_date": "2027-05-20T14:00:00",
  "location": "Аудитория 12",
  "accessibility": "субтитры, текстовый чат"
}
```

## Ответы и ошибки
- Успешная регистрация: HTTP 201, объект пользователя и поле token.
- Неверные входные данные: HTTP 400.
- Неверные учётные данные: HTTP 401.
- Отсутствующий или недействительный токен: HTTP 401.
- Недостаточно прав: HTTP 403.
- Мероприятие или запись не найдены: HTTP 404.
- Повторная регистрация или повторный отзыв: HTTP 409.

Пароли хранятся в виде хеша. Не передавайте пароль в URL и не помещайте секреты в репозиторий.
