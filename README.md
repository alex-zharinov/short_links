### Short Links

[![short-links workflow](https://github.com/alex-zharinov/short_links/actions/workflows/main.yml/badge.svg)](https://github.com/alex-zharinov/short_links/actions/workflows/main.yml)

## Сервис сокращения ссылок и его API
> Назначение сервиса — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.

## Технологии проекта:
- Python — высокоуровневый язык программирования;
- SQLAlchemy — это Python-библиотека, которая позволяет работать с реляционными базами данных с помощью ORM;
- Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2.

### Как запустить проект:
- Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/alex-zharinov/short_links.git
```
```
cd short_links
```
- Cоздать и активировать виртуальное окружение:
```
python3 -m venv venv
```
* Если у вас Linux/macOS
    ```
    source venv/bin/activate
    ```
* Если у вас windows
    ```
    source venv/scripts/activate
    ```
- Создать .env. Пример:
```
#  ./.env

FLASK_APP=short_links
FLASK_ENV=development
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=Secret
```
- Запустить проект:
```
flask run
```

### Ваш проект будет доступен по ссылке:
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)
На сайте можно заполнить форму для получения короткой ссылки. Предложить свой варинт ссылки является опцией.

### API для проекта
API проекта доступен всем желающим. Сервис обслуживает только два эндпоинта:
- `/api/id/` — POST-запрос на создание новой короткой ссылки;
- `/api/id/<short_id>/` — GET-запрос на получение оригинальной ссылки по указанному короткому идентификатору.
Примеры запросов к API, варианты ответов и ошибок приведены в спецификации openapi.yml; спецификация есть в репозитории.
Для удобной работы с документом воспользуйтесь онлайн-редактором Swagger Editor, в котором можно визуализировать спецификацию.

### Пример запроса:
```
 - curl -X POST http://127.0.0.1:5000/api/id/
   -H 'Content-Type: application/json'
   -d '{"url": "https://thepythoncode.com/", "custom_id": "thepy1"}'
```
Sample responce:
```
{
    "short_link": "http://127.0.0.1:5000/thepy1",
    "url": "https://thepythoncode.com/"
}
```

## Автор
[Жаринов Алексей](https://github.com/alex-zharinov)
