# API AccessEvent

Защищённые запросы используют заголовок `Authorization: Bearer <token>`. JWT действует 24 часа.

| Метод | Путь | Доступ | Назначение |
|---|---|---|---|
| GET | /health | Публичный | Состояние сервиса |
| POST | /api/auth/register | Публичный | Регистрация |
| POST | /api/auth/login | Публичный | Вход |
| POST | /api/register | Публичный | Совместимый маршрут регистрации |
| POST | /api/login | Публичный | Совместимый маршрут входа |
| GET | /api/events | Публичный | Каталог; параметры q, accessibility |
| GET | /api/events/{id} | Публичный | Детали события |
| POST | /api/events | organizer/admin | Создание события |
| POST | /api/events/{id}/register | Авторизованный | Запись на событие |
| DELETE | /api/events/{id}/register | Авторизованный | Отмена записи |
| GET | /api/my/registrations | Авторизованный | Мои регистрации |
| PATCH | /api/registrations/{id} | organizer/admin | Изменение статуса заявки |
| GET, POST | /api/events/{id}/messages | Авторизованный | Текстовый чат |
| GET, POST | /api/events/{id}/reviews | GET публичный; POST авторизованный | Отзывы |
| GET | /api/notifications | Авторизованный | Просмотр уведомлений |

Пароли хранятся только в виде хеша. Не передавайте пароль в URL.