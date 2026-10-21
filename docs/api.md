<<<<<<< HEAD
# Описание API AccessEvent
(См. методичку День 5)
=======
# API AccessEvent

Защищённые запросы используют заголовок Authorization: Bearer <token>. JWT действует 24 часа.

| Метод | Путь | Доступ | Назначение |
|---|---|---|---|
| GET | /health | Публичный | Состояние сервиса |
| POST | /api/auth/register | Публичный | Регистрация |
| POST | /api/auth/login | Публичный | Вход |
| GET | /api/events | Публичный | Каталог; параметры q, accessibility |
| GET | /api/events/{id} | Публичный | Детали события |
| POST | /api/events | organizer/admin | Создание события |
| POST | /api/events/{id}/register | Авторизованный | Запись |
| GET | /api/me/registrations | Авторизованный | Мои регистрации |

Пароли хранятся только в виде хеша. Не передавайте пароль в URL.
>>>>>>> 93f660917251956e4d1be85cd249fe95ff9b5fe6
