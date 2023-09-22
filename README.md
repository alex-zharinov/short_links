[![short-links workflow](https://github.com/alex-zharinov/short_links/actions/workflows/main.yml/badge.svg)](https://github.com/alex-zharinov/short_links/actions/workflows/main.yml)

## Укорачивание ссылок

> Проект YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.

## Технологии проекта

- Python — высокоуровневый язык программирования.
- Flask - фреймворк для создания веб-приложений на языке программирования Python

### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

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

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать .env. Пример:

```
FLASK_APP=yacut
FLASK_ENV=development
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=Secret
```

Запустить проект:

```
flask run
```

Проект будет доступен по ссылке http://127.0.0.1:5000/
Там вы сможете заполнить форму для получения короткой ссылки. Предложить свой варинт ссылки является опцией.

Доступ к API осуществляется по http://127.0.0.1:5000/api/id/

Пример запроса:
{
  "url": "https://thepythoncode.com/",
  "custom_id": "thepy1"
}
Ответ:
{
    "short_link": "http://127.0.0.1:5000/thepy1",
    "url": "https://thepythoncode.com/"
}

Более подробно ознакомиться с докуметацией - openapi.yml

## Автор
[Жаринов Алексей](https://github.com/alex-zharinov)
