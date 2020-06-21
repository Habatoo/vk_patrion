# Backend часть проекта VK.Творцы
***
## Структура проекта:
```
|--/migrations # папки миграции БД

|--/app

|   |--/static

|   |--/img

|   |--/js

|   |--/user_data # папки для загрузки контента пользователями

|   |     |--/vk0000000000 # папка тестового пользователя

|   |--__init__.py # инициализация приложения

|   |--models.py # sqlalchemy модели, структура таблиц с описанием полей для БД

|   |--view.py # доступные api 

|--.gitignore

|--app.db # файл БД, создается при запуске

|--app.log # файл логирования, создается при запуске

|--config.py # файл настроек конфигурации flask 

|--main.py # точка входа, файл запуска приложения 

|--Procfile # файл конфигурации для heroku

|--README.md # файл ридми

|--requirements.txt # список всех установленных библиотек с их зависимостями
```
***
## Установка и запуск:
```
git clone git@github.com:Habatoo/vk_patrion.git
cd vk_patrion
pip install -r requirements.txt
flask run
```

смена порта в файле main.py ```app.run(host='0.0.0.0', port=8080)```
***
## Админка:
После установки по локальному [адресу](http://localhost:5000/admin) доступна панель администратора, для создания и изменения информации по:
 - контенту [Content](http://localhost:5000/admin/content)
 - пользователям [User](http://localhost:5000/admin/user)
 - тэгам - темам контанта и интересам польователей [Tag](http://localhost:5000/admin/tag)
***
## API:
Доступные API, тестирование проводится с помощью curl:
- создание пользователя c vk id - vk3333333333, с тегом (интересами) translation:

```curl -i -H "Content-Type: application/json" http://localhost:5000/api/create_user/vk3333333333/translation```

- создание текстового контента пользователем с vk id - vk3333333333, с темой title, содержимым body, и тегом translation:
```curl -i -H "Content-Type: application/json" http://localhost:5000/api/create_text_content/vk3333333333/title/body/translation```

- создание файлового контента пользователем с vk id - vk3333333333, с темой title, ссылки на скачивание fileurl, и тегом music:

```curl -i -H "Content-Type: application/json" http://localhost:5000/api/create_file_content/vk3333333333/title/fileurl/music```

- запрос списка всех пользователей:

```curl -i -H "Content-Type: application/json" http://localhost:5000/api/users```

- запрос пользователя с c vk id - vk3333333333 и всего его контента:

```curl -i -H "Content-Type: application/json" http://localhost:5000/api/user/vk3333333333```

- запрос всего контента всех пользователей:

```curl -i -H "Content-Type: application/json" http://localhost:5000/api/contents```

- запрос содержимого контента с id 1:

```curl -i -H "Content-Type: application/json" http://localhost:5000/api/content/1```
 



