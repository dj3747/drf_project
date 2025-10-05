# drf_project

## Веб-приложение: Платформа для онлайн-обучения

## Установка:
1. Клонируйте репозиторий `git@github.com:dj3747/drf_project.git`
2. Инициализируйте `poetry init` и установите зависимости после обновления `pyproject.toml` командой `poetry install`
3. Создайте файл `.gitignore`
4. Подключили СУБД `PostgreSOL` для работы в проекте
5. Установите `Drf`
6. Для тестирования используйте `Postman`, `unittest`
7. Для фильтрации установлен `django-filter`
8. Добавлена библиотека `djangorestframework-simplejwt`
9. Настроено использование `JWT-авторизации`
10. Добавлены валидаторы,пагинация и тесты на основе `unittest`
11. Подключён и настроен вывод документации для проекта
12. Для работы с документацией проекта использована библиотека `drf-yasg`
13. Подключена возможность оплаты курсов через `https://stripe.com/docs/api`
14. В проекте настроена система обработки задач в фоновом режиме `Celery` 
  и установлен пакет для периодических задач `celery-beat`


## Запуск проекта через `Docker-Compose`
1. Клонируйте репозиторий `git@github.com:dj3747/drf_project.git`
2. Создать файл `.env`
3. Собрать контейнеры `docker-compose build`
4. Запустить контейнеры `docker-compose up -d`
5. Выполнить миграции `docker-compose exec web python manage.py migrate`
6. Создать суперпользователя `docker-compose exec web python manage.py createsuperuser`
7. Собрать статические файлы `docker-compose exec web python manage.py collectstatic --noinput`
8. Открыть проект. Приложение доступно по адресу: http://localhost:8000
9. Остановка контейнеров `docker-compose down`
10. Логи контейнера `docker-compose logs -f web`


## Запуск `Ci/CD`
1. Выполняется при `push` или `pull request` ветки `feature/homework`
2. Прогоняются тесты на Python 3.13
3. При успехе запускается автоматический `deploy` на сервер
4. Сервер: http://158.160.188.89
5. Доступ осуществляется через SSH-ключи, хранящиеся в `GitHub Secrets`



## Структура проекта
Проект состоит из следующих пакетов и приложений:

1.`config` - пакет с базовыми настройками
2.Приложение - `users`
3.Приложение - `education`

## Лицензия:
Проект распространяется под [лицензией MIT](LICENSE)